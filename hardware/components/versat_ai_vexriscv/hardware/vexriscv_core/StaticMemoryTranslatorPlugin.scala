package vexriscv.plugin

import vexriscv.{VexRiscv, _}
import spinal.core._
import spinal.lib._

import scala.collection.mutable.ArrayBuffer
case class StaticMemoryTranslatorPort(bus : MemoryTranslatorBus, priority : Int)

class StaticMemoryTranslatorPlugin(ioRange : UInt => Bool) extends Plugin[VexRiscv] with MemoryTranslator {
  val portsInfo = ArrayBuffer[StaticMemoryTranslatorPort]()

  var ioStartAddr : UInt = null
  var ioSize : UInt = null
  var ioEndAddr : UInt = null

  override def newTranslationPort(priority : Int,args : Any): MemoryTranslatorBus = {
    val port = StaticMemoryTranslatorPort(MemoryTranslatorBus(MemoryTranslatorBusParameter(wayCount = 0)),priority)
    portsInfo += port
    port.bus
  }

  override def setup(pipeline: VexRiscv): Unit = {
    if(ioRange == null) {
      // Define the input parameters for IO (uncached) range
      ioStartAddr = in(UInt(32 bits).setName("ioStartAddr"))
      ioSize = in(UInt(32 bits).setName("ioSize"))
      // Calculate the end address of IO range
      ioEndAddr = ioStartAddr + ioSize - 1
    }
  }

  override def build(pipeline: VexRiscv): Unit = {
    import pipeline._
    import pipeline.config._
    import Riscv._

    val core = pipeline plug new Area {
      val ports = for ((port, portId) <- portsInfo.zipWithIndex) yield new Area {
        port.bus.rsp.physicalAddress := port.bus.cmd.last.virtualAddress
        port.bus.rsp.allowRead := True
        port.bus.rsp.allowWrite := True
        port.bus.rsp.allowExecute := True
        // Function determines if given address is in IO range configured via inputs
        val externalIoRange: UInt => Bool = (address: UInt) => {
          address >= ioStartAddr && address <= ioEndAddr
        }
        if(ioRange != null) 
          port.bus.rsp.isIoAccess := ioRange(port.bus.rsp.physicalAddress)
        else
          port.bus.rsp.isIoAccess := externalIoRange(port.bus.rsp.physicalAddress)
        port.bus.rsp.isPaging := False
        port.bus.rsp.exception := False
        port.bus.rsp.refilling := False
        port.bus.busy := False
      }
    }
  }
}
