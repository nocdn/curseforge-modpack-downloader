import requests
import json
import os
from urllib.parse import quote
import argparse
from tqdm import tqdm


def build_download_url(file_id: int, file_name: str) -> str:
    dir1 = file_id // 1000
    dir2 = f"{file_id % 1000:03d}"
    encoded = quote(file_name)
    return f"https://mediafilez.forgecdn.net/files/{dir1}/{dir2}/{encoded}"


def download_file(file_id: int, file_name: str, dest_folder: str = ".") -> None:
    url = build_download_url(file_id, file_name)
    path = os.path.join(dest_folder, file_name)

    os.makedirs(dest_folder, exist_ok=True)

    print(f"downloading {file_name} -> {path}")
    print(f"cdn url: {url}")

    try:
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            block_size = 8192
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=file_name, leave=False)
            with open(path, "wb") as fh:
                for chunk in r.iter_content(chunk_size=block_size):
                    if chunk:
                        progress_bar.update(len(chunk))
                        fh.write(chunk)
            progress_bar.close()
            if total_size != 0 and progress_bar.n != total_size:
                 print("error: download incomplete")
                 return
        print(f"\ndownload complete: {path}")
        print("you can now remove the directory this script is in")
    except Exception as e:
        if 'progress_bar' in locals() and not progress_bar.disable:
            progress_bar.close()
        print(f"error downloading file: {e}")


def return_search_results(query: str) -> dict | None:
    url = (
        "https://www.curseforge.com/api/v1/mods/search"
        f"?gameId=432&index=0&classId=4471"
        f"&filterText={quote(query)}"
        "&pageSize=20&sortField=2"
    )
    headers = {"accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"error fetching search results: {e}")
        return None


def get_files_list(project_id: int) -> dict | None:
    url = f"https://www.curseforge.com/api/v1/mods/{project_id}/files"
    headers = {"accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"error fetching files list: {e}")
        return None


def get_additional_files(project_id: int, file_id: int) -> dict | None:
    url = f"https://www.curseforge.com/api/v1/mods/{project_id}/files/{file_id}/additional-files"
    headers = {"accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"error fetching additional files: {e}")
        return None


def choose_from_list(items, label_key, id_key):
    if not items:
        print("no items to choose from.")
        return None
    for idx, itm in enumerate(items):
        # Format index with leading zero padding to 2 digits (:02d)
        print(f"[{idx:02d}] {itm.get(label_key, 'n/a')} [id: {itm.get(id_key, 'n/a')}]")
    while True:
        choice = input("select index: ")
        try:
            # int() naturally handles inputs like "07" -> 7 or "7" -> 7
            i = int(choice)
            if 0 <= i < len(items):
                return items[i]
            else:
                 print(f"invalid index. please enter a number between 0 and {len(items)-1}.")
        except ValueError:
            print("invalid input. please enter a number.")


def main():
    parser = argparse.ArgumentParser(description="download modpacks from curseforge.")
    parser.add_argument("-s", "--search", help="modpack search query (skips interactive search)")
    parser.add_argument("-o", "--output", default=".", help="output directory for downloaded files (default: current directory)")
    args = parser.parse_args()

    query = args.search if args.search else input("search curseforge for: ")
    if not query:
        print("search query cannot be empty.")
        return

    search_res = return_search_results(query)
    if not search_res or "data" not in search_res or not search_res["data"]:
        print(f"no results found for '{query}'")
        return

    chosen_project = choose_from_list(search_res["data"], "name", "id")
    if not chosen_project:
        return

    project_id = chosen_project["id"]
    files_res = get_files_list(project_id)
    if not files_res or "data" not in files_res or not files_res["data"]:
        print("no files found for this project")
        return

    chosen_file = choose_from_list(files_res["data"], "displayName", "id")
    if not chosen_file:
        return

    file_id     = chosen_file["id"]
    file_name   = chosen_file["fileName"]
    output_dir  = args.output

    if chosen_file.get("hasServerPack"):
        mode = input("download normal (n) or server pack (s)? [n]: ").lower().strip() or "n"
        if mode == "s":
            add_res = get_additional_files(project_id, file_id)
            if not add_res or "data" not in add_res or not isinstance(add_res["data"], list) or not add_res["data"]:
                print("no server packs found or error fetching them.")
                print("falling back to normal download...")
                download_file(file_id, file_name, output_dir)
                return
            print("server files available:")
            if len(add_res["data"]) > 1:
                 chosen_sp = choose_from_list(add_res["data"], "displayName", "id")
            elif len(add_res["data"]) == 1:
                 chosen_sp = add_res["data"][0]
                 print(f"selected: {chosen_sp['displayName']}")
            else:
                 print("no valid server pack data found.")
                 return

            if not chosen_sp:
                return
            print(f"downloading server pack {chosen_sp['fileName']}")
            download_file(chosen_sp["id"], chosen_sp["fileName"], output_dir)
            return

    download_file(file_id, file_name, output_dir)

if __name__ == "__main__":
    main()