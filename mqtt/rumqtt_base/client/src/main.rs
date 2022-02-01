use tokio::{task, time};

use rumqttc::{self, AsyncClient, MqttOptions, QoS};
use std::error::Error;
use std::time::Duration;

#[tokio::main(worker_threads = 1)]
async fn main() -> Result<(), Box<dyn Error>> {
    pretty_env_logger::init();
    // color_backtrace::install();

    let mut mqttoptions = MqttOptions::new("test-1", "localhost", 1883);
    mqttoptions.set_keep_alive(Duration::from_secs(5));

    let (client, mut eventloop) = AsyncClient::new(mqttoptions, 10);
    task::spawn(async move {
        requests(client).await;
        time::sleep(Duration::from_secs(3)).await;
    });

    loop {
        let event = eventloop.poll().await;
        println!("{:?}", event.unwrap());
    }
}

async fn requests(client: AsyncClient) {
    client
        .subscribe("GENERICO-CORPO/JSON/0/1/ADDITIVE-MANUFACTURING-12/PRINT/1", QoS::AtMostOnce)
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
            .publish("hello/world", QoS::ExactlyOnce, false, payload)
            .await
            .unwrap();

        time::sleep(Duration::from_secs(1)).await;
    }

    time::sleep(Duration::from_secs(120)).await;
}
