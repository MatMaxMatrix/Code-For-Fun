import torch 
from torch import nn


class Encoder(nn.Module):
    def __init__(self, input_channels, hidden_dim, embed_dim):
        """
        Costruttore della classe Encoder
        params:
            - input_channels : canali delle immagini di input
            - hidden_dim : dimensione degli hidden layer
            - embed_dim : dimensione degli encodings
        """
        super().__init__()
        # layer di ingresso che trasforma i canali di ingresso in canali degli hidden layers
        self.in_layer = nn.Sequential(
            nn.Conv2d(input_channels, input_channels, 5, padding='same'),
            nn.Conv2d(input_channels, hidden_dim, 1),
            nn.ReLU()
        )

        # hidden layers convoluzionali
        self.hidden_layers = nn.Sequential(
            nn.Conv2d(hidden_dim, hidden_dim, 5, padding='same'),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), 

            nn.Conv2d(hidden_dim, hidden_dim, 5, padding='same'),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), 

            nn.Conv2d(hidden_dim, hidden_dim, 5, padding='same'),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), 
        )

        # Layer di encoding
        self.encoding_layer = nn.Sequential(
            nn.Conv2d(hidden_dim, embed_dim, 3, padding='same'),
            nn.Tanh()
        )

    def forward(self, x):
        z = self.in_layer(x)
        z = self.hidden_layers(z)
        y = self.encoding_layer(z)
        return y


class AutoEncoder(nn.Module):
    def __init__(self, input_channels, hidden_dim, embed_dim):
        super().__init__()
        self.encoder = Encoder(input_channels, hidden_dim, embed_dim)
        
        # Decoder speculare all'encoder
        self.decoder = nn.Sequential(
            nn.Conv2d(embed_dim, hidden_dim, 3, padding='same'),
            nn.ReLU(),
            
            nn.ConvTranspose2d(hidden_dim, hidden_dim, 2, stride=2),
            nn.ReLU(),
            
            nn.ConvTranspose2d(hidden_dim, hidden_dim, 2, stride=2),
            nn.ReLU(),
            
            nn.ConvTranspose2d(hidden_dim, hidden_dim, 2, stride=2),
            nn.ReLU(),
            
            nn.Conv2d(hidden_dim, input_channels, 5, padding='same'),
            nn.Sigmoid()
        )

    def forward(self, x):
        z = self.encoder(x)
        y = self.decoder(z)
        return y 
    
    def encode(self, image):
        # funzione per effettuare una codifica dell'immagine
        encodings = self.encoder(image)
        return encodings