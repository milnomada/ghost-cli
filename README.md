# Ghost Cli
A Python client for [Ghost]()

## Configuration

Create a Custom Integration as explained [here](https://ghost.org/docs/admin-api/#token-authentication).  
The Integration will provide the Admin API Key. Create the `GHOST_KEY` environment variable with the value of the admin key:
```
export GHOST_KEY="633391e30a8cba0bc1e96f20:a12bc792cd9ed482d4a7d1da2c045e5261feae2181fab4d8dad0d93f7e34bc82"
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
