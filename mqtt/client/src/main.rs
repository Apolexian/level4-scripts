// Adapted from https://github.com/bytebeamio/rumqtt/blob/master/rumqttc/examples/syncpubsub.rs
use quic_socket::{QuicClient, QuicSocket};
use rumqttc::{self, AsyncClient, MqttOptions, QoS};
use std::env;
use tokio::{task, time};
use std::time::Duration;

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
        .subscribe("GENERICO-CORPO/JSON/0/1/ADDITIVE-MANUFACTURING-13/PRINT/1", QoS::AtMostOnce)
        .await
        .unwrap();
    let payload = "\"print\" = {
        \"Timestamp\"=\"20201001 171035\",
        \"BedTemp\"=\"75\",
        \"ExtruderTemp\"=\"205\",
        \"Adhesion\"=\"Skirt\",
        \"File\"=\"/home/prints/base.gcode\",
        \"Speed\"=\"50 mm/s\",
        \"Layer Height\"=\"0.12 mm\",
        \"Retraction\"=\"6mm at 25mm/s\",
        \"Infill\"=\"20%\",
        \"Initial layer speed\"=\"20 mm/s\",
        \"Initial fan speed\"=\"0%\"
    }".as_bytes();
    for _ in 1..=100 {
        client
            .publish("GENERICO-CORPO/JSON/0/1/ADDITIVE-MANUFACTURING-13/PRINT/1", QoS::ExactlyOnce, false, payload)
            .await
            .unwrap();

        time::sleep(Duration::from_secs(1)).await;
    }

    time::sleep(Duration::from_secs(120)).await;
}
