# Skii platform

- **Api server** using [Django Ninja](https://github.com/vitalik/django-ninja)
- **Vitejs frontend** using [Vuejs](https://vuejs.org/)

## Features

- User management with profile (student/teacher)
- Planning management with schedule lesson
- Location promote and location
- Lesson level and certification

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
<img src="docsite/public/poneyninja.png" alt="" />
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
```
