docker run --init -d \
  --name homeassistant \
  --restart=unless-stopped \
  -e TZ=Europe/Brussels \
  -v /Users/ekeneattoh/Documents/Portfolio_and_Personal_Documents/Personal_Development/PhD/PhD_Docs/eattoh-phd/iot_middleware_mvp/home_assistant_test/config/:/config \
  -p 8123:8123 homeassistant_ea:latest