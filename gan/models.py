import torch
from gan.spectral_normalization import SpectralNorm

class Discriminator(torch.nn.Module):
    def __init__(self, input_channels=3):
        super(Discriminator, self).__init__()
        
        #Hint: Hint: Apply spectral normalization to convolutional layers. Input to SpectralNorm should be your conv nn module
        ####################################
        #          YOUR CODE HERE          #
        ####################################
        self.conv1 = SpectralNorm(torch.nn.Conv2d(3, 128, kernel_size = 4, stride = 2, padding = 1))
        self.conv2 = SpectralNorm(torch.nn.Conv2d(128, 256, kernel_size = 4, stride = 2, padding = 1))
        self.bn1 = torch.nn.BatchNorm2d(256)
        self.conv3 = SpectralNorm(torch.nn.Conv2d(256, 512, kernel_size = 4, stride = 2, padding = 1))
        self.bn2 = torch.nn.BatchNorm2d(512)
        self.conv4 = SpectralNorm(torch.nn.Conv2d(512, 1024, kernel_size = 4, stride = 2, padding = 1))
        self.bn3 = torch.nn.BatchNorm2d(1024)
        self.conv5 = SpectralNorm(torch.nn.Conv2d(1024, 1, kernel_size = 4, stride = 1, padding = 1))
        self.leaky_relu = torch.nn.LeakyReLU(0.2)
        
        ##########       END      ##########
    
    def forward(self, x):
        
        ####################################
        #          YOUR CODE HERE          #
        ####################################
        x = self.leaky_relu(self.conv1(x))
        x = self.leaky_relu(self.bn1(self.conv2(x)))
        x = self.leaky_relu(self.bn2(self.conv3(x)))
        x = self.leaky_relu(self.bn3(self.conv4(x)))
        x = self.conv5(x)
        
        ##########       END      ##########
        
        return x


class Generator(torch.nn.Module):
    def __init__(self, noise_dim, output_channels=3):
        super(Generator, self).__init__()    
        self.noise_dim = noise_dim
        
        ####################################
        #          YOUR CODE HERE          #
        ####################################
        self.conv1 = torch.nn.ConvTranspose2d(self.noise_dim, 1024, kernel_size = 4, stride = 1)
        self.bn1 = torch.nn.BatchNorm2d(1024)
        self.conv2 = torch.nn.ConvTranspose2d(1024, 512, kernel_size = 4, stride = 2, padding = 1)
        self.bn2 = torch.nn.BatchNorm2d(512)
        self.conv3 = torch.nn.ConvTranspose2d(512, 256, kernel_size = 4, stride = 2, padding = 1)
        self.bn3 = torch.nn.BatchNorm2d(256)
        self.conv4 = torch.nn.ConvTranspose2d(256, 128, kernel_size = 4, stride = 2, padding = 1)
        self.bn4 = torch.nn.BatchNorm2d(128)
        self.conv5 = torch.nn.ConvTranspose2d(128, 3, kernel_size = 4, stride = 2, padding = 1)
        
        ##########       END      ##########
    
    def forward(self, x):
        
        ####################################
        #          YOUR CODE HERE          #
        ####################################
        # x = x.view(128, self.noise_dim , 1, 1)
        # j, k = x.size()
        # x = x.reshape(j, k)

        x = torch.nn.functional.relu(self.bn1(self.conv1(x)))
        x = torch.nn.functional.relu(self.bn2(self.conv2(x)))
        x = torch.nn.functional.relu(self.bn3(self.conv3(x)))
        x = torch.nn.functional.relu(self.bn4(self.conv4(x)))
        x = torch.tanh(self.conv5(x))
        
        ##########       END      ##########
        
        return x
    

