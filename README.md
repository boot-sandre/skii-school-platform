# Skii platform

- **Api server** using [Django Ninja](https://github.com/vitalik/django-ninja)
- **Vitejs frontend** using [Vuejs](https://vuejs.org/)

## Features

- User management with profile (student/teacher)
- Planning management with scheduled lesson
- Place/Skii station promote and location
- Lesson level and certification (TODO)

<details>
<summary>:books: Read the <a href="https://boot-sandre.github.io/skii-school-platform">documentation</a></summary>

 - [Get started](https://boot-sandre.github.io/django-spaninja/get_started)
    - [Install and run](https://boot-sandre.github.io/django-spaninja/get_started/install_and_run)
 - [Base app](https://boot-sandre.github.io/django-spaninja/base_app)
     - [Forms](https://boot-sandre.github.io/django-spaninja/base_app/forms)
        - [Usage](https://boot-sandre.github.io/django-spaninja/base_app/forms/usage)
     - [Schemas](https://boot-sandre.github.io/django-spaninja/base_app/schemas)
 - [Account app](https://boot-sandre.github.io/django-spaninja/account_app)
     - [Endpoints](https://boot-sandre.github.io/django-spaninja/account_app/endpoints)
     - [Schemas](https://boot-sandre.github.io/django-spaninja/account_app/schemas)
     - [Utilities](https://boot-sandre.github.io/django-spaninja/account_app/utilities)
         - [Email](https://boot-sandre.github.io/django-spaninja/account_app/utilities/email)
         - [Token](https://boot-sandre.github.io/django-spaninja/account_app/utilities/token)

</details>

<div align="center">
<img src="docsite/public/skiiplatform.png" alt="Skii Platform Logo" />
</div>

## Development 

### Code quality

This project uses [Pycheck](https://github.com/emencia/pycheck) to monitor the quality of the code. To install
the code quality tools:

```bash
make install-pycheck
# or
yarn global add @pycheck/cli
yarn global add @pycheck/ui
# or
npm install -g @pycheck/cli
npm install -g @pycheck/ui
```

#### Analysis and history

Run:

```bash
pycheckui
```

Open `localhost:5143` in a browser to run an analysis. Note: this uses a `.pycheck.db` local Sqlite file
to store the code quality history

#### Command line

To do a quick check in the command line (not recorded in history):

```bash
pycheck
# or
make pycheck
```
#### Unittest

To launch full set of project unittest

```bash
make test
```

#### Install

To install project on a local dev environment
```bash
make install
# Also if need to be logged
make superuser
```

#### Launch and access

To launch
```bash
make run
```

To access api docs you need to follow http://localhost:8000/skii/docs
To access django admin you need to http://localhost:8000/admin/

#### Enjoy

All skii source code is licensed with mozilla MPL 2 and all new source python file needs to integrate this headers
```python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
```

Enjoy and use it :P
