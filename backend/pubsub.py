import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

# Required for configuring our application to use PubNub
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-7c05ce8e-61ab-11ea-aaa3-eab2515ceb0d'
pnconfig.publish_key = 'pub-c-d7e75e4e-3274-4017-83d4-e940969268e1'

TEST_CHANNEL = 'TEST_CHANNEL'

# Class Listener inherits the SubscribeCallback functionality thus allowing us to override their methods to make it specific to our application.
class Listener(SubscribeCallback):
  def message(self, pubnub, message_object):
      print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

    
class PubSub():
  """
  Handles the publish/subscribe layer of the application.
  Provides communication between the nodes of the network.
  """
  def __init__(self):
    self.pubnub = PubNub(pnconfig)
    self.pubnub.subscribe().channels([TEST_CHANNEL]).execute()
    self.pubnub.add_listener(Listener())

  def publish(self, channel, message):
    """
    Publish the message object to the channel.
    """
    self.pubnub.publish().channel(channel).message(message).sync()


def main():
  pubsub = PubSub()
  time.sleep(1)
  pubsub.publish(TEST_CHANNEL, { "name": "ZajdelCoin" })


if __name__ == '__main__':
  main()




