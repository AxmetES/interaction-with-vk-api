## Script for publish image on vk group wall by API

Project for publish images to vk group on the wall by VK API [vk Developers](https://vk.com/dev),
from the  [comics site](https://xkcd.com/) by json [service](https://xkcd.com/json.html)

## Getting Started

For the project to work, install all necessary packages from `requirements.txt`.

```python
pip install -r requirements.txt
```

For work with API register and get the ACCESS_TOKEN from the (https://vk.com/dev/implicit_flow_user)

```python
ACCESS_TOKEN='your key'
GROUP_ID='your group id'
```
you extract it in the code.

```python
import os
from dotenv import load_dotenv
```

## Motivation

The project is an assignment in online courses [Devman](https://dvmn.org/modules/).

## Running

The script is run from the command line.

```python
python main.py
```

## License

You may copy, distribute and modify the software.
