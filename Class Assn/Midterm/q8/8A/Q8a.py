if __name__ == '__main__':
    import matplotlib.pyplot as plt  # for plotting
    import numpy as np  # for transformation

    import torch  # PyTorch package
    import torchvision  # load datasets
    import torchvision.transforms as transforms  # transform data
    import torch.nn as nn  # basic building block for neural neteorks
    import torch.nn.functional as F  # import convolution functions like Relu
    import torch.optim as optim  # optimzer
    import time

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    transform = transforms.Compose(  # composing several transforms together
        [transforms.ToTensor(),  # to tensor object
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])  # mean = 0.5, std = 0.5

    # set batch_size
    batch_size = 10

    # set number of workers
    num_workers = 2

    # load train data
    trainset = torchvision.datasets.ImageFolder(root='./train', transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=num_workers)

    # load test data
    testset = torchvision.datasets.ImageFolder(root='./test', transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    # put classes into a set
    classes = ('crop', 'weed')


    def imshow(img, true, pred):
        ''' function to show image '''
        trueTop = []
        trueBottom = []
        predTop = []
        predBottom = []
        i = 0
        for x in true:
            if(i < 5):
                trueTop.append(x)
            else:
                trueBottom.append(x)
            i+=1
        i=0
        for x in pred:
            if(i < 5):
                predTop.append(x)
            else:
                predBottom.append(x)
            i+=1

        title = "Actual: " + str(trueTop) + "\n           " + str(trueBottom) + "\n\nPrdct : " + str(predTop) + "\n           " + str(predBottom)
        img = img / 2 + 0.5  # unnormalize
        npimg = img.numpy()  # convert to numpy objects
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.title(title)
        plt.show()


    class Net(nn.Module):
        ''' Models a simple Convolutional Neural Network'''

        def __init__(self):
            ''' initialize the network '''
            super(Net, self).__init__()
            # 3 input image channel, 6 output channels,
            # 5x5 square convolution kernel
            self.conv1 = nn.Conv2d(3, 6, 5)
            # Max pooling over a (2, 2) window
            self.pool = nn.MaxPool2d(2, 2)
            self.conv2 = nn.Conv2d(6, 16, 5)
            self.fc1 = nn.Linear(16 * 125 * 125, 120)  # 5x5 from image dimension     breaks
            self.fc2 = nn.Linear(120, 84)
            self.fc3 = nn.Linear(84, 2)

        def forward(self, x):
            ''' the forward propagation algorithm '''
            # print('x_shape:', x.shape)
            x = self.pool(F.relu(self.conv1(x)))
            # print('x_shape:', x.shape)
            x = self.pool(F.relu(self.conv2(x)))
            # print('x_shape:', x.shape)
            x = x.view(-1, 16 * 125 * 125)
            # print('x_shape:', x.shape)
            x = F.relu(self.fc1(x))  # breaks here
            # print('x_shape:', x.shape)
            x = F.relu(self.fc2(x))
            # print('x_shape:', x.shape)
            x = self.fc3(x)
            # print('x_shape:', x.shape)
            return x


    net = Net()
    print(net)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    if torch.cuda.is_available():
        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        start.record()
    startTime = time.time()

    printHeader = False
    for epoch in range(2):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()

            if i % 20 == 19:
                if not printHeader:
                    printHeader = True
                    print("[Epoch, Batch]")
                # print every 64 mini-batches
                print('[%d,     %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 64))
                running_loss = 0.0

    # whatever you are timing goes here
    if torch.cuda.is_available():
        # Waits for everything to finish running
        torch.cuda.synchronize()
    print('Finished Training')
    endTime = time.time() - startTime
    print(str(endTime) + "seconds")

    # save
    PATH = './CropWeedModel.pth'
    torch.save(net.state_dict(), PATH)
    # reload
    # net = Net()
    # net.load_state_dict(torch.load(PATH))

    dataiter = iter(testloader)
    images, labels = dataiter.next()

    # print images

    print('True result: ', ' '.join('%s' % classes[labels[j]] for j in range(10)))

    outputs = net(images)

    _, predicted = torch.max(outputs, 1)

    print('Predicted: ', ' '.join('%s' % classes[predicted[j]] for j in range(10)))
    labelTrue = []
    labelPred = []
    for i in range(10):
        labelTrue.append(classes[labels[i]])
        labelPred.append(classes[predicted[i]])

    imshow(torchvision.utils.make_grid(images, nrow=5), labelTrue, labelPred)

    correct = 0
    total = 0
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print('Accuracy of the network on the 10 test images: %d %%' % (100 * correct / total))
