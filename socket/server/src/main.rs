use quic_socket::{QuicServer, QuicSocket};
use tokio;

#[tokio::main]
async fn main() {
    // quic_socket::gen_certificates().unwrap();
    let addr = "127.0.0.1:4442".parse().unwrap();
    let mut server = QuicServer::new(Some(addr)).await;
    let mut buf = [0; 200];
    let payload = vec![6; 100];
    let read = server.recv(&mut buf).await.unwrap();
    let read2 = server.recv(&mut buf).await.unwrap();
    server.send(payload).await.unwrap();
    println!("{:?}", read);
    println!("{:?}", read2);
}
