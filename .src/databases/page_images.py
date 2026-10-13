# Schema reference for page_images table.
# Actual definition lives in models.py — keep this file in sync when fields change.
#
# page_images
#   id          integer  primary key (auto)
#   page_id     integer  references pages.id  not null
#   image       string   pydal upload filename
#   description string   max 500 chars
#   position    integer  default 0
