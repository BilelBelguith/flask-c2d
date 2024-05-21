import requests
from bs4 import BeautifulSoup
  
GITLAB_URL = ''
GITLAB_TOKEN = ''

def fetch_all_groups():
    try:
        response = requests.get(f'{GITLAB_URL}/api/v4/groups?private_token={GITLAB_TOKEN}')
        groups = response.json()
        group_list = [group['full_path'] for group in groups]
        group_count = len(groups)
        return group_list, group_count
    except Exception as e:
        print(f'Error fetching groups: {e}')
        return [], 0

def fetch_all_users():
    user_list = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        try:
            response = requests.get(f'{GITLAB_URL}/api/v4/users?private_token={GITLAB_TOKEN}&page={page}')
            data = response.json()

            if isinstance(data, list):
                user_list.extend([user['email'] for user in data])
            else:
                print(f'Error fetching users: {data}')
                break

            total_pages = int(response.headers.get('X-Total-Pages'), 10) or 1
            page += 1
        except Exception as e:
            print(f'Error fetching users: {e}')
            break

    user_count = len(user_list)
    return user_list, user_count

def filter_groups(value, options):
    return [option for option in options if value.lower() in option.lower()]

def filter_users(value, options):
    return [option for option in options if value.lower() in option.lower()]

if __name__ == '__main__':
    # Fetch all groups and users
    groups, group_count = fetch_all_groups()
    users, user_count = fetch_all_users()

    # Filtered values (replace with the actual input values)
    group_value = 'c'
    user_value = 'o'

    # Example usage of filtering
    filtered_groups = filter_groups(group_value, groups)
    filtered_users = filter_users(user_value, users)

    # Print the results
    print(f'Groups: {filtered_groups} (Count: {group_count})')
    print(f'Users: {filtered_users} (Count: {user_count})')
