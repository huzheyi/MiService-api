# MiService

XiaoMi Cloud Service for mi.com support api (自用)
This is a fork from https://github.com/yihong0618/MiService and https://github.com/Yonsm/MiService

Thanks to @yihong0618 and @Yonsm

## 本地运行

为了方便与其他系统整合调用miservice的服务，加了一个server.py，用以支持api调用

```
pip install aiohttp mutagen rich fastapi pydantic uvicorn
python server.py
```

## Docker运行

```
docker pull ghcr.io/huzheyi/miservice-api:latest
#docker pull huzheyi/miservice-api:latest

docker run -itd \
  --name miservice-api \
  -e MI_USER="YourMIUser" \
  -e MI_PASS="YourMIPass" \
  -e MI_DID="YourMIDid" \
  -p 8000:8000 \
  miservice-api:latest
```

> 接口文档 http://localhost:8000/docs (FastAPI自动生成)