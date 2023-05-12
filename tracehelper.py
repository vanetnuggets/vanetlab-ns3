
import context

def enable_trace(ifc, name):
    """
      @ifc interface
      @name name of the file
    """
    print('ns3 trace', context.path + name + '_asciitrace.txt created for', name)
    ascii = ns.network.AsciiTraceHelper()
    stream = ascii.CreateFileStream(context.path + '/' + name + '_asciitrace.txt')

    ifc.EnableAsciiAll(stream)
    ifc.EnablePcapAll(name)
