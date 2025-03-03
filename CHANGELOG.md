# Changelog

## 0.4.0 (2025-03-03)

### Feat

- override like and comment for virtual doctype
- move all interfaces into abc folder
- add new ClientSideController and ClientSideContext
- add RestModelMapper to enable robust mapping
- add ClientSidePaginator implementation

### Fix

- fixing docker-compose.yaml
- fix missing import error
- update RedisDocumentMetadata to use the enum
- fixing some minor bugs RestModelMapper

### Refactor

- update app name and add some interfaces

## 0.3.0 (2025-02-22)

### Feat

- add example usage from JSON Placeholder API
- add new RestContext and VirtualContext
- **controllers/rest_controller**: add implementation of RestController and edit some configurations
- fixing docker-compose, Dockerfile scripts and update docs
- add working Dockerfile and docker-compose.yaml
- add not working docker-compose.yaml
- add docker-compose.yaml
- update docs and add virtual doctype classes

### Fix

- **formatter**: fixing .editorconfig and prettier conflict

## 0.2.0 (2025-02-12)

### Feat

- setup minimal frappe template
- Initialize App

### Fix

- **.pre-commit-config.yaml**: update exclude to none fixing the commitizen hooks
- fixing asset wrong import
- remove onscan deps and replace using Joi
