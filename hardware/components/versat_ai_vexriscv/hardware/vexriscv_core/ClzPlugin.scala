package vexriscv.demo

import spinal.core._
import vexriscv.plugin.Plugin
import vexriscv.{Stageable, DecoderService, VexRiscv}

object ClzPlugin {
  // this is trying to look like DOI 10.2478/jee-2015-0054
  def fun_clz_NLCi(x:Bits): Bits = {
      val r2 = (~(x(0) | x(1) | x(2) | x(3)))
      val r1 = (~(x(2) | x(3)))
      val r0 = (~(x(3) | (x(1) & ~x(2))))
      val r = r2 ## r1 ## r0
      r // return value
  }
  def fun_clz_BNE(a:Bits) : Bits = {
      val a01 = ~(a(0) & a(1))
      val a23 = ~(a(2) & a(3))

      val a45 = ~(a(4) & a(5))
      val a67 = ~(a(6) & a(7))

      val a0123 = ~(a01 | a23) // also r(2)
      val a4567 = ~(a45 | a67)

      val a56 = ~(a(5) & ~a(6))
      val a024 = (a(0) & a(2) & a(4)) // AND not NAND
      val a13 = ~(a(1) & a(3))
      val a12 = ~(a(1) & ~a(2))
      
      val r3 = ((a0123 & a4567)) // AND not NAND
      val r2 = (a0123)
      val r1 = (~(a01 | (~a23 & a45)))
      val r0 = (~((~((a56) & (a024))) & (~((a13) & (a12) & (a(0))))))

      val r = r3 ## r2 ## r1 ##r0
      
      r // return value
  }
  def fun_clz(in:Bits) : Bits = {
    val nlc7 = fun_clz_NLCi(in(31 downto 28))
    val nlc6 = fun_clz_NLCi(in(27 downto 24))
    val nlc5 = fun_clz_NLCi(in(23 downto 20))
    val nlc4 = fun_clz_NLCi(in(19 downto 16))
    val nlc3 = fun_clz_NLCi(in(15 downto 12))
    val nlc2 = fun_clz_NLCi(in(11 downto  8))
    val nlc1 = fun_clz_NLCi(in( 7 downto  4))
    val nlc0 = fun_clz_NLCi(in( 3 downto  0))
    val a = nlc0(2) ## nlc1(2) ## nlc2(2) ## nlc3(2) ## nlc4(2) ## nlc5(2) ## nlc6(2) ## nlc7(2)
    val bne = fun_clz_BNE(a)
      
    val muxo = (bne(2 downto 0)).mux(
      B"3'b000" -> nlc7(1 downto 0),
      B"3'b001" -> nlc6(1 downto 0),
      B"3'b010" -> nlc5(1 downto 0),
      B"3'b011" -> nlc4(1 downto 0),
      B"3'b100" -> nlc3(1 downto 0),
      B"3'b101" -> nlc2(1 downto 0),
      B"3'b110" -> nlc1(1 downto 0),
      B"3'b111" -> nlc0(1 downto 0)
    )
    val r = (bne(3)) ?  B"6'b100000" | (B"1'b0" ## bne(2 downto 0) ## muxo(1 downto 0)) // 6 bits
    
    r.resize(32) // return value
  }
}

class ClzPlugin(earlyInjection : Boolean = true) extends Plugin[VexRiscv]{
  import ClzPlugin._
  object IS_CLZ extends Stageable(Bool)
  object OUTPUT extends Stageable(Bits(32 bits))

  //Callback to setup the plugin and ask for different services
  override def setup(pipeline: VexRiscv): Unit = {
    import pipeline.config._

    //Retrieve the DecoderService instance
    val decoderService = pipeline.service(classOf[DecoderService])

    //Specify the IS_CLZ default value when instruction are decoded
    decoderService.addDefault(IS_CLZ, False)

    //Specify the instruction decoding which should be applied when the instruction match the 'key' parttern
    decoderService.add(
      //Bit pattern of the new IS_CLZ instruction
      key = M"011000000000-----001-----0010011",

      //Decoding specification when the 'key' pattern is recognized in the instruction
      List(
        REGFILE_WRITE_VALID      -> True, //Enable the register file write
        BYPASSABLE_EXECUTE_STAGE -> Bool(earlyInjection), //Notify the hazard management unit that the instruction result is already accessible in the EXECUTE stage (Bypass ready)
        BYPASSABLE_MEMORY_STAGE  -> True, //Same as above but for the memory stage
        RS1_USE -> True, //Notify the hazard management unit that this instruction use the RS1 value
        IS_CLZ -> True,
        SRC1_CTRL                -> Src1CtrlEnum.RS
      )
    )
  }

  override def build(pipeline: VexRiscv): Unit = {
    import pipeline._
    import pipeline.config._

    //Add a new scope on the execute stage (used to give a name to signals)
    execute plug new Area {
      import execute._
      //Define signal used internally to the plugin
      insert(OUTPUT) := fun_clz(input(SRC1)).asBits
    } // execute plug newArea

    val injectionStage = if(earlyInjection) execute else memory
		injectionStage plug new Area {
			import injectionStage._
			when (arbitration.isValid && input(IS_CLZ)) {
				output(REGFILE_WRITE_DATA) := input(OUTPUT)
			} // when input is
		} // injectionStage plug newArea
  } // override def build
} // class Plugin