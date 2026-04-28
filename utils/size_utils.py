def format_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024

    return f"{size:.1f} {units[-1]}"