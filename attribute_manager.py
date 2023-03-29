from ns import ns
from log_helper import dbg

class AttributeManager:
  _defaults = {
    'RxGain': 16.0,
    'TxGain': 16.0,
    'MaxPackets': 1,
    'MaxBytes': 1024,
    'PacketSize': 1024,
    'MaxPackets': 1024,
    'Interval': 1,
  }

  def __init__(self):
    pass
  
  def default(self, attr):
    if attr not in self._defaults:
      raise Exception(f'attribute {attr} does not have a default value.')
    return self.get_val_for(attr, self._defaults[attr])

  def get_val_for(self, attr, value):
    if attr in ['RxGain', 'TxGain']:
      return ns.core.DoubleValue(float(value))
    
    if attr in ['MaxBytes', 'MaxPackets']:
      return ns.core.UintegerValue(value)
    
    if attr in ['']:
      return None
    
    raise Exception(f'cannot get attribute class for {attr}')

  def install_attributes(self, item, helper, attr_field='attributes', method='Set'):
    if 'attributes' in item:
      for attr in item['attributes']:
        val = item['attributes'][attr]
        dbg.log(f'installing attribute {attr} for value {val}')

        if method == 'Set':
          helper.Set(attr, self.get_val_for(attr, val))
        else:
          helper.SetAttribute(attr, self.get_val_for(attr, val))

  def clear_attributes(self, item, helper, method='Set'):
    if 'attributes' in item:
      for attr in item['attributes']:
        if method == 'Set':
          helper.Set(attr, self.default(attr))
        else:
          helper.SetAttribute(attr, self.default(attr))

attribute_manager = AttributeManager()