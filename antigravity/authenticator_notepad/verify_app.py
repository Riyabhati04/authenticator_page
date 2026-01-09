import urllib.request
import urllib.parse
import http.cookiejar
import sys

BASE_URL = "http://127.0.0.1:5000"
EMAIL = "urllib_test@example.com"
PASSWORD = "urllibpassword"

# Setup cookie jar
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def run_test(name, func):
    print(f"Running {name}...", end=" ")
    try:
        func()
        print("PASS")
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

def test_signup():
    url = f"{BASE_URL}/signup"
    data = urllib.parse.urlencode({'email': EMAIL, 'password': PASSWORD}).encode()
    try:
        with opener.open(url, data=data) as response:
            content = response.read().decode('utf-8')
            # Should be on login page
            if "Login" not in content and "Sign Up" not in content:
                raise Exception("Did not redirect to login page properly")
    except urllib.error.HTTPError as e:
        raise Exception(f"Signup HTTP Error: {e.code}")

def test_login():
    url = f"{BASE_URL}/login"
    data = urllib.parse.urlencode({'email': EMAIL, 'password': PASSWORD}).encode()
    try:
        with opener.open(url, data=data) as response:
            content = response.read().decode('utf-8')
            if "My Tasks" not in content:
                raise Exception("Did not redirect to dashboard. Login might have failed.")
    except urllib.error.HTTPError as e:
        raise Exception(f"Login HTTP Error: {e.code}")

def test_create_task():
    url = f"{BASE_URL}/task/create"
    data = urllib.parse.urlencode({'title': 'Urllib Task 1'}).encode()
    try:
        with opener.open(url, data=data) as response:
            content = response.read().decode('utf-8')
            if "Urllib Task 1" not in content:
                raise Exception("Task not found in dashboard after creation")
    except urllib.error.HTTPError as e:
        raise Exception(f"Create Task HTTP Error: {e.code}")

if __name__ == "__main__":
    try:
        # Check if server is up
        try:
            with urllib.request.urlopen(BASE_URL) as response:
                pass
        except urllib.error.URLError:
            print("Server is not running!")
            sys.exit(1)

        run_test("Signup", test_signup)
        run_test("Login", test_login)
        run_test("Create Task", test_create_task)
        print("\nAll automated verification tests passed!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
