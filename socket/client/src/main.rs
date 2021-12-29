use quic_socket::{QuicClient, QuicSocket};
use tokio;

#[tokio::main]
async fn main() {
    let mut client = QuicClient::new(None).await;
    let mut buf = [0; 200];
    let payload = vec![6; 100];
    let payload2 = vec![6; 150];
    client.send(payload).await.unwrap();
    client.send(payload2).await.unwrap();
    let read = client.recv(&mut buf).await.unwrap();
    println!("{:?}", read);
}
