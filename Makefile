start:
	docker-compose up --build -d

stop:
	docker-compose down

agent-start:
	docker-compose exec etl-video-encoding prefect agent start dev

prefect-reset:
	docker-compose exec etl-video-encoding prefect orion database reset -y

apply-deploy:
	docker-compose exec etl-video-encoding prefect deployment apply deploy/video_encoding.yaml
