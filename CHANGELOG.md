# Changelog

<!--next-version-placeholder-->

## v1.0.1 (2022-04-09)
### Fix
* **github actions:** Added poetry add flake8 to ci pipeline. Other minor fixes. ([`fe0f605`](https://github.com/sunnydsouza/notion-api-py/commit/fe0f605890cf6698c5347b129acea3af45290996))
* **pyproject:** Removed flake8 from package dependencies ([`02316b5`](https://github.com/sunnydsouza/notion-api-py/commit/02316b508977cac24398f6d11628ce39347f1dcc))
* **pyproject:** Removed flake8 from package dependencies ([`f4eded1`](https://github.com/sunnydsouza/notion-api-py/commit/f4eded152cd85af34629323b813ba3d204f5c79a))


## v1.0.0 (2022-04-08)
### Feature
* **notion_collection_view_filter:** Added ability to dynamically set filters on Notion UI (unoffical api) ([`6950998`](https://github.com/sunnydsouza/notion-api-py/commit/69509988d4e3f6242e0d7cfcce2787ae5b0266bd))
* **notion_collection_view_filter:** Added ability to dynamically set filters on Notion UI (unoffical api) ([`db9171c`](https://github.com/sunnydsouza/notion-api-py/commit/db9171c502028c808ec26d126dfe49856b60f55e))
* **notion_filter:** Ability to apply filter on notion databases in very human friendly way ([`79b6182`](https://github.com/sunnydsouza/notion-api-py/commit/79b6182767afd7528358991a316034dd866c3384))
* **notion_relation:** Added class to handle notion relations. Helps overwrite/append to existing relations in database. ([`9013436`](https://github.com/sunnydsouza/notion-api-py/commit/90134362c4c2e301c741b67eb53b20eebc3101e3))
* **notion_properties:** Added class that allows one to read properties from any database page and also dynamically generate json body request (used in api calls) ([`1bf98bf`](https://github.com/sunnydsouza/notion-api-py/commit/1bf98bfcd1ac3d2b3e19f705301c466bb0106e4f))
* **notion_page:** A wrapper notion page class which gives update/delete/fetch properties capabilities to any class that extends it. ([`6446340`](https://github.com/sunnydsouza/notion-api-py/commit/64463402f861b1b1030aab26573679800b0a5b55))
* **notion_database:** A wrapper notion database class which gives basic add/delete/update/filter capabilites to any class that extends it. ([`a0e44a4`](https://github.com/sunnydsouza/notion-api-py/commit/a0e44a41a7a9fd29317bd1239156569cbc5fc6b1))
* **notion-api:** Added base wrapper around the notion endpoints per version 2021-08-16 (https://developers.notion.com/reference) ([`fe44760`](https://github.com/sunnydsouza/notion-api-py/commit/fe4476029f27dace642014d2f346d7a123a009fd))

### Breaking
* Added ability to dynamically set filters on Notion UI (unoffical api)  ([`6950998`](https://github.com/sunnydsouza/notion-api-py/commit/69509988d4e3f6242e0d7cfcce2787ae5b0266bd))

### Documentation
* **README:** Updated readme with initial usage instructions. ([`6a508bb`](https://github.com/sunnydsouza/notion-api-py/commit/6a508bbb4998e7454f885e16ac9dbac3a2f1eba0))
* **README:** Updated readme with initial usage instructions. ([`8f7a6cb`](https://github.com/sunnydsouza/notion-api-py/commit/8f7a6cbd5b86cfeab2fd0e932f66c4a060cc2db7))
