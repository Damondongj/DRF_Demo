from confluent_kafka import Producer

# Kafka 服务器配置
bootstrap_servers = 'localhost:9092'

# 创建 Producer 实例
producer = Producer({'bootstrap.servers': bootstrap_servers})

# Kafka 主题
topic = 'your_topic'

# 发送消息到 Kafka
for i in range(10000):
    producer.produce(topic, value='Hello, Kafka!')

# 刷新消息队列以确保消息被发送
producer.flush()

# 关闭 Producer
producer.close()
