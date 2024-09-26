from pathlib import Path

import yaml

from pigeon.caveman import DumpyMcDumpface


def merge_list_with_dicts_based_on_key(
    list1: list[dict], list2: list[dict], **kwargs
) -> list[dict]:
    seen_keys = set()
    merged_list = []

    for entry in list1 + list2:
        key_value = entry.get(kwargs.get("key"))
        if key_value not in seen_keys:
            seen_keys.add(key_value)
            merged_list.append(entry)

    return merged_list


def merge(into: dict, values: dict) -> dict:
    merged = into.copy()
    for k, v in values.items():
        if k not in merged:
            merged[k] = v
        else:
            existing = merged[k]
            if isinstance(existing, dict):
                merged[k] = merge(existing, v)
            elif isinstance(existing, list):
                # Don't really like this, would very much appreciate nicer
                # suggestions on how to go about this if there are any
                if k == "collaborators":
                    usernames = set()
                    deduped = []
                    for entry in existing + v:
                        name = entry.get("username")
                        if name not in usernames:
                            usernames.add(name)
                            deduped.append(entry)
                    merged[k] = deduped
                else:
                    merged[k].extend(v)
            else:
                merged[k] = v
    return merged


def main():
    with Path("pigeon/ports.yml").open("r", encoding="utf-8") as portsYml, Path(
        "pigeon/userstyles.yml"
    ).open("r", encoding="utf-8") as userstylesYml:
        ports = yaml.safe_load(portsYml)
        userstyles = yaml.safe_load(userstylesYml)

    with Path("pigeon/merged.yml").open("w", encoding="utf-8") as f:
        yaml.dump(
            merge(ports, userstyles),
            stream=f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            Dumper=DumpyMcDumpface,
        )


if __name__ == "__main__":
    main()
