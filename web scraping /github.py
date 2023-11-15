import requests
import csv


def get_all_repositories(token=None):
    # GitHub API endpoint for public repositories
    api_url = 'https://api.github.com/repositories'

    # Optional: Add a personal access token for authentication
    headers = {}
    if token:
        headers['Authorization'] = f'Token {token}'

    # Initialize the list to store all repositories
    all_repositories = []

    # Loop through paginated responses until there are no more pages
    page = 1
    while True:
        # Send an HTTP GET request to the GitHub API
        response = requests.get(api_url, headers=headers, params={'page': page, 'per_page': 100})

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            repositories = response.json()

            # Add the repositories from the current page to the list
            all_repositories.extend(repositories)

            # Check if there are more pages
            if len(repositories) < 100:
                break

            # Increment the page number for the next request
            page += 1
        else:
            print(f"Error: {response.status_code}")
            break

    return all_repositories


def save_to_csv(data, filename='github_repositories.csv'):
    # Specify the CSV file header
    fields = ['id', 'name', 'full_name', 'owner', 'html_url', 'description', 'created_at', 'updated_at', 'pushed_at']

    # Write data to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # Write the header
        writer.writeheader()

        # Write the data
        for repo in data:
            # Extract only the desired fields from the repository dictionary
            repo_data = {field: repo.get(field, '') for field in fields}
            writer.writerow(repo_data)


# Optional: If you have a personal access token, provide it here
# token = 'your_personal_access_token'
token = None

# Get all public repositories on GitHub
repositories = get_all_repositories(token)

# Save the repository information to a CSV file
save_to_csv(repositories, 'github_repositories.csv')

print("CSV file created successfully.")
