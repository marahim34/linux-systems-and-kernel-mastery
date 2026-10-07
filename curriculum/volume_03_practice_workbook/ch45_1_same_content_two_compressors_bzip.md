1. Same content, two compressors. bzip2 (.tbz) is usually a bit smaller but slower to create. ls -l shows the byte
difference.

7c. Why -C matters
# -C makes archived paths relative (tmp/...),
# so extraction cannot overwrite absolute system paths
# and works safely in any target directory.