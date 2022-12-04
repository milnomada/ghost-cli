# Ghost Cli &nbsp; &nbsp;<img src="https://d33wubrfki0l68.cloudfront.net/9a4849ff454e5eaa1b2f5ff885049b494f4f739a/5a3b4/assets/images/tool-icons/ghost.png" alt="drawing" align="top" height="35px"/>



A Python client for [Ghost](https://ghost.org/docs/)

![Cov](./assets/cov.svg)
![GitHub tag](https://img.shields.io/github/v/tag/milnomada/ghost-cli)

## About

Ghost-cli is a mininal client library for Ghost, thought to ease the management of Ghost resources for programmatic tasks.  
It makes use of client credentials from a [Custom Integration](https://ghost.org/integrations/custom-integrations/) that must be created to configure the client.

Ghost-cli implements CRUD operations on the following models:
| Name     | Doc                                          |
|----------|----------------------------------------------|
| Post     | https://ghost.org/docs/admin-api/#posts      |
| Tag      | https://ghost.org/docs/content-api/#tags     |
| Author   | https://ghost.org/docs/content-api/#authors  |

Integration with Newsletters, Members or other resources of Ghost are not available.


## Configuration

Create a Custom Integration as explained [here](https://ghost.org/docs/admin-api/#token-authentication).  
The Integration will provide the Admin API Key, use it as value to create the `GHOST_KEY` environment variable:
```
export GHOST_KEY="633391e30a8cba0bc1e96f20:a12bc792cd9ed482d4a7d1da2c045e5261feae2117fab4d8dad0d93f7e34bc82"
```

## Install

```bash
pip install git+https://github.com/milnomada/ghost-cli.git#egg=ghost-cli
```

## Usage

```python
from ghost_cli import GhostCli, Tokener

tokener = Tokener()
token = tokener.generate()
cli = GhostCli("http://my.ghost.io", token)
cli.create_post(title="hello world")

post = cli.get_post_by_title("hello world")
print(f"{post.title}, {post.slug}, {post.published_at}, {post.created_at}")
post = cli.get_post("slug", "hello-world")

updated = cli.update_post(post.id, title="Hello World Auth", updated_at=post.updated_at)
print(f"updated: {updated}")
```
