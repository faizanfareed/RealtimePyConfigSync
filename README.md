# RealtimePyConfigSync
Real-time detection and loading of dynamic configuration changes from an etcd database to a Python process.

[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/20px-Python-logo-notext.svg.png">](https://www.python.org)
[![Generic badge](https://img.shields.io/badge/license-MIT-success.svg)](https://shields.io/)
[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) 

---

Instead of `periodically pooling configurations` from a `database` at `fixed intervals`, we can utilize `etcd database` 
to `watch for changes` on specific keys (configs). Whenever `new changes occur` on these keys, the `etcd server` will push those changes 
to the `client`, and then `react` on them accordingly.

---

Under the hood, it utilizes the `python-etcd3` library, which provides a callback method to listen for changes on keys.

#### Here are some additions made :


-    No `boilerplate code` is required.
-    There is `no need` to manually define which `callback function type` needs to be bound.
-    It provides a `JSON deserializer` by default, but you can define your own deserialization logic based on your requirements.
-    It supports `auto-reconnection` with etcd in case of a connection failure.
-    You can specify the `number of connection retries` and the `retry delay`.
-    It applies `different deserialization` methods to keys if you `have mixed key-value` pairs.
-    It allows for easy addition of `new observers` to perform desired operations on keys.
-    You can remove the `parse_engine` observer in case of `simple key-value pairs`.


---

## etcd 
 A distributed, reliable key-value store for the most critical data of a distributed system. etcd is a CNCF project.

 [Read more about etcd ](https://etcd.io/)

---
## Requirements 
 
- [Python](https://www.python.org/downloads/)
- [etcd](https://etcd.io/)
- [Etcd Manager](https://snapcraft.io/install/etcd-manager/ubuntu) - Optional 

---

## Installation

Clone the Repository

1. Open your terminal or command prompt.
2. Change to the directory where you want to clone the project.
3. Execute the following command to clone the repository:

```shell
git clone https://github.com/faizanfareed/RealtimePyConfigSync.git
```


### Setup

Navigate to the project directory:

```shell
cd RealtimePyConfigSync
```

Create a virtual environment (optional but recommended):

For venv:

```shell
python -m venv env
```

For virtualenv:
```shell
virtualenv env
```

Activate the virtual environment:

For Windows:

```shell
.\env\Scripts\activate
```
For Unix/macOS:
```shell
source env/bin/activate
```

Install the project dependencies:
```shell
pip install -r requirements.txt
```

---

### Run etcd server as a Docker 

https://hub.docker.com/r/bitnami/etcd/

Once your Docker is up and running, open the app.py module and update the configurations there. 
After making the necessary changes, run the module.

--- 

### Install etcd manager on ubuntu 

https://snapcraft.io/install/etcd-manager/ubuntu

---

## License

[![Generic badge](https://img.shields.io/badge/license-MIT-success.svg)](https://shields.io/)

License under a [MIT License](https://choosealicense.com/licenses/mit/)

python-etcd3 license  [Apache License 2.0](https://github.com/kragniz/python-etcd3/blob/master/LICENSE).

---

## Contributing 

- Fork, clone or make a pull request to this repository. 
- Ask here  [https://github.com/faizanfareed/RealtimePyConfigSync/discussions](https://github.com/faizanfareed/RealtimePyConfigSync/discussions)


