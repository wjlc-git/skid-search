import requests
import random
import time
import sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt

console = Console()

GITHUB_API = "https://api.github.com/search/repositories"
HEADERS = {"Accept": "application/vnd.github.v3+json"}


def skid_search_menu():
    console.print("[bold cyan]Welcome to Skid Search CLI[/bold cyan]")
    while True:
        console.print("\n[bold yellow]Options:[/bold yellow]")
        console.print("1. Search In Text")
        console.print("2. Search In Title")
        console.print("3. Source Code Extract")
        console.print("4. Larp Tool")
        console.print("5. Exit")

        choice = IntPrompt.ask("Enter your choice")

        if choice == 1:
            search_github("text")
        elif choice == 2:
            search_github("title")
        elif choice == 3:
            source_code_extract()
        elif choice == 4:
            skid_tool()
        elif choice == 5:
            console.print("Exiting... Peace skid 😎")
            break
        else:
            console.print("[red]Invalid option[/red]")


def search_github(mode):
    query = Prompt.ask("Enter search phrase")
    query_str = f"{query} in:description,readme stars:>200" if mode == "text" else f"{query} in:name stars:>200"

    params = {
        "q": query_str,
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    console.print("[bold green]Searching GitHub...[/bold green]")
    res = requests.get(GITHUB_API, headers=HEADERS, params=params)

    if res.status_code == 200:
        items = res.json().get("items", [])
        if not items:
            console.print("[yellow]No matching repositories found.[/yellow]")
        for repo in items:
            console.print(f"[blue]{repo['html_url']}[/blue] - ⭐ {repo['stargazers_count']}")
    else:
        console.print(f"[red]GitHub API error: {res.status_code}[/red]")


def source_code_extract():
    repo_url = Prompt.ask("Enter full GitHub repository URL (e.g., https://github.com/user/repo)")
    if not repo_url.startswith("https://github.com/"):
        console.print("[red]Invalid GitHub URL[/red]")
        return

    path_parts = repo_url.replace("https://github.com/", "").split("/")
    if len(path_parts) < 2:
        console.print("[red]Invalid GitHub repository path[/red]")
        return

    user, repo = path_parts[0], path_parts[1]
    contents_api = f"https://api.github.com/repos/{user}/{repo}/contents/"

    res = requests.get(contents_api)
    if res.status_code != 200:
        console.print("[red]Failed to fetch repository contents[/red]")
        return

    files = res.json()
    py_files = [f for f in files if f["type"] == "file"]

    if not py_files:
        console.print("[yellow]No files found in repository.[/yellow]")
        return

    console.print("\n[bold green]Files in repo:[/bold green]")
    for idx, file in enumerate(py_files):
        console.print(f"{idx + 1}. {file['name']}")

    choice = IntPrompt.ask("Choose file number to extract")
    try:
        selected = py_files[choice - 1]
        code_res = requests.get(selected["download_url"])
        console.print(f"\n[bold blue]Source code for {selected['name']}:[/bold blue]\n")
        console.print(code_res.text)
    except:
        console.print("[red]Invalid file selection[/red]")


def skid_tool():
    console.print("[bold magenta]Larp Tool[/bold magenta]")
    for _ in range(10000):
        fake_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        status = random.choice(["hacked", "breached", "backdoored", "doomed"])
        console.print(f"{fake_ip} - [green]{status}[/green]")
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        skid_search_menu()
    except KeyboardInterrupt:
        console.print("\n[red]Exited by user.[/red]")
        sys.exit()
