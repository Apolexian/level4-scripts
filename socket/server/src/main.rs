use quic_socket::QuicSocket;
use tokio;

#[tokio::main]
async fn main() {
    let addr = "0.0.0.0:4444".parse().unwrap();
    let socket = QuicSocket::bind(addr).await.unwrap();
    let con_addr = "0.0.0.0:4443".parse().unwrap();
    let mut listener = socket.connect(con_addr).unwrap();
    let mut buf = [0; 65535];
    loop {
        let read = match listener.recv(&mut buf).await {
            Ok(r) => r,
            Err(e) => {
                println!("{:?}", e);
                return;
            }
        };
        println!("{:?}", &buf[..read])
    }
}
