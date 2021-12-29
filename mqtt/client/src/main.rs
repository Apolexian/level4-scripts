// Adapted from https://github.com/bytebeamio/rumqtt/blob/master/rumqttc/examples/syncpubsub.rs
use quic_socket::{QuicClient, QuicSocket};
use rumqttc::{self, AsyncClient, MqttOptions, QoS};
use std::env;
use tokio::{task};

#[tokio::main(worker_threads = 1)]
async fn main() {
    let addr = "127.0.0.1:5000".parse().unwrap();
    pretty_env_logger::init();
    let args: Vec<String> = env::args().collect();
    let ip = &args[1];
    let client = QuicClient::new(None).await;
    let mut mqttoptions = MqttOptions::new("test-1", ip, 1883, addr, client);
    mqttoptions.set_connection_timeout(10);
    mqttoptions.set_keep_alive(5);

    let (client, mut eventloop) = AsyncClient::new(mqttoptions, 100);
    task::spawn(async move {
        requests(client).await;
    });

    loop {
        let event = eventloop.poll().await;
        println!("{:?}", event.unwrap());
    }
}

async fn requests(client: AsyncClient) {
    client
        .subscribe(format!("topic0"), QoS::AtMostOnce)
        .await
        .unwrap();
    for i in 0..100 {
        client
            .publish("topic0", QoS::AtMostOnce, true, vec![1; i])
            .await
            .unwrap();
    }
}
