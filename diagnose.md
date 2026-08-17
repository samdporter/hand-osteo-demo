### Issue with pip in docker container

can be fixed with 
```
docker buildx rm holoscan_app_builder
docker buildx create --name holoscan_app_builder --driver docker-container --bootstrap
```
And verified with
```
docker exec buildx_buildkit_holoscan_app_builder0 cat /etc/resolv.conf
```

Note: Used Claude for this fix