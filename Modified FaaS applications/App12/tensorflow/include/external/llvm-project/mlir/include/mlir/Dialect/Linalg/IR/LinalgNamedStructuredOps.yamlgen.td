
//===----------------------------------------------------------------------===//
// Op definition for MatmulOp
//===----------------------------------------------------------------------===//

def MatmulOp : LinalgStructuredBase_Op<"matmul", !listconcat([
  AttrSizedOperandSegments,
  DeclareOpInterfaceMethods<MemoryEffectsOpInterface>,
  SingleBlockImplicitTerminator<"YieldOp">],
  /*extraInterfaces=*/[LinalgContractionOpInterface])> {
    
  let summary = [{ Performs a matrix multiplication of two 2D inputs. }];
  let description = [{
    Numeric casting is performed on the operands to the inner multiply, promoting
them to the same data type as the accumulator/output.
  }];

    let arguments = (ins
      Variadic<AnyType>:$inputs,
      Variadic<AnyShaped>:$outputs
    );
    let results = (outs Variadic<AnyRankedTensor>:$result_tensors);
    let regions = (region AnyRegion:$region);

    let skipDefaultBuilders = 1;
    let builders = [
      OpBuilder<
      (ins "ValueRange":$inputs, "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<MatmulOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$inputs,
            "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addTypes(resultTensorTypes);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<MatmulOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$operands,
            CArg<"ArrayRef<NamedAttribute>", "{}">:$attributes),
      [{
        $_state.addOperands(operands);
        $_state.addAttributes(attributes);
        $_state.addTypes(resultTensorTypes);
        (void)$_state.addRegion();
      }]>
      
    ];
    let printer = [{ return ::printNamedStructuredOp(p, *this); }];
    let parser = [{
      return ::parseNamedStructuredOp<MatmulOp>(parser, result);
    }];
    let hasFolder = 1;

    let extraClassDeclaration = structuredOpsBaseDecls # [{
      // Auto-generated.
      ArrayAttr iterator_types();
      ArrayAttr indexing_maps();
      static void regionBuilder(
        ImplicitLocOpBuilder &b, Block &block, ValueRange captures);
      static std::function<
        void(ImplicitLocOpBuilder &b, Block &, ValueRange)>
      getRegionBuilder() {
        return regionBuilder;
      }

      // Generic methods.
      static unsigned getNumRegionArgs();
      std::string getLibraryCallName();
      
    }];
}

//===----------------------------------------------------------------------===//
// Op definition for BatchMatmulOp
//===----------------------------------------------------------------------===//

def BatchMatmulOp : LinalgStructuredBase_Op<"batch_matmul", !listconcat([
  AttrSizedOperandSegments,
  DeclareOpInterfaceMethods<MemoryEffectsOpInterface>,
  SingleBlockImplicitTerminator<"YieldOp">],
  /*extraInterfaces=*/[LinalgContractionOpInterface])> {
    
  let summary = [{ Performs a batched matrix multiplication of two 3D inputs. }];
  let description = [{
    Numeric casting is performed on the operands to the inner multiply, promoting
them to the same data type as the accumulator/output.
  }];

    let arguments = (ins
      Variadic<AnyType>:$inputs,
      Variadic<AnyShaped>:$outputs
    );
    let results = (outs Variadic<AnyRankedTensor>:$result_tensors);
    let regions = (region AnyRegion:$region);

    let skipDefaultBuilders = 1;
    let builders = [
      OpBuilder<
      (ins "ValueRange":$inputs, "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<BatchMatmulOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$inputs,
            "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addTypes(resultTensorTypes);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<BatchMatmulOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$operands,
            CArg<"ArrayRef<NamedAttribute>", "{}">:$attributes),
      [{
        $_state.addOperands(operands);
        $_state.addAttributes(attributes);
        $_state.addTypes(resultTensorTypes);
        (void)$_state.addRegion();
      }]>
      
    ];
    let printer = [{ return ::printNamedStructuredOp(p, *this); }];
    let parser = [{
      return ::parseNamedStructuredOp<BatchMatmulOp>(parser, result);
    }];
    let hasFolder = 1;

    let extraClassDeclaration = structuredOpsBaseDecls # [{
      // Auto-generated.
      ArrayAttr iterator_types();
      ArrayAttr indexing_maps();
      static void regionBuilder(
        ImplicitLocOpBuilder &b, Block &block, ValueRange captures);
      static std::function<
        void(ImplicitLocOpBuilder &b, Block &, ValueRange)>
      getRegionBuilder() {
        return regionBuilder;
      }

      // Generic methods.
      static unsigned getNumRegionArgs();
      std::string getLibraryCallName();
      
    }];
}

//===----------------------------------------------------------------------===//
// Op definition for MatvecOp
//===----------------------------------------------------------------------===//

def MatvecOp : LinalgStructuredBase_Op<"matvec", !listconcat([
  AttrSizedOperandSegments,
  DeclareOpInterfaceMethods<MemoryEffectsOpInterface>,
  SingleBlockImplicitTerminator<"YieldOp">],
  /*extraInterfaces=*/[LinalgContractionOpInterface])> {
    
  let summary = [{ Performs a matrix-vector multiplication. }];
  let description = [{
    Numeric casting is performed on the operands to the inner multiply, promoting
them to the same data type as the accumulator/output.
  }];

    let arguments = (ins
      Variadic<AnyType>:$inputs,
      Variadic<AnyShaped>:$outputs
    );
    let results = (outs Variadic<AnyRankedTensor>:$result_tensors);
    let regions = (region AnyRegion:$region);

    let skipDefaultBuilders = 1;
    let builders = [
      OpBuilder<
      (ins "ValueRange":$inputs, "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<MatvecOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$inputs,
            "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addTypes(resultTensorTypes);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<MatvecOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$operands,
            CArg<"ArrayRef<NamedAttribute>", "{}">:$attributes),
      [{
        $_state.addOperands(operands);
        $_state.addAttributes(attributes);
        $_state.addTypes(resultTensorTypes);
        (void)$_state.addRegion();
      }]>
      
    ];
    let printer = [{ return ::printNamedStructuredOp(p, *this); }];
    let parser = [{
      return ::parseNamedStructuredOp<MatvecOp>(parser, result);
    }];
    let hasFolder = 1;

    let extraClassDeclaration = structuredOpsBaseDecls # [{
      // Auto-generated.
      ArrayAttr iterator_types();
      ArrayAttr indexing_maps();
      static void regionBuilder(
        ImplicitLocOpBuilder &b, Block &block, ValueRange captures);
      static std::function<
        void(ImplicitLocOpBuilder &b, Block &, ValueRange)>
      getRegionBuilder() {
        return regionBuilder;
      }

      // Generic methods.
      static unsigned getNumRegionArgs();
      std::string getLibraryCallName();
      
    }];
}

//===----------------------------------------------------------------------===//
// Op definition for VecmatOp
//===----------------------------------------------------------------------===//

def VecmatOp : LinalgStructuredBase_Op<"vecmat", !listconcat([
  AttrSizedOperandSegments,
  DeclareOpInterfaceMethods<MemoryEffectsOpInterface>,
  SingleBlockImplicitTerminator<"YieldOp">],
  /*extraInterfaces=*/[LinalgContractionOpInterface])> {
    
  let summary = [{ Performs a vector-matrix multiplication. }];
  let description = [{
    Numeric casting is performed on the operands to the inner multiply, promoting
them to the same data type as the accumulator/output.
  }];

    let arguments = (ins
      Variadic<AnyType>:$inputs,
      Variadic<AnyShaped>:$outputs
    );
    let results = (outs Variadic<AnyRankedTensor>:$result_tensors);
    let regions = (region AnyRegion:$region);

    let skipDefaultBuilders = 1;
    let builders = [
      OpBuilder<
      (ins "ValueRange":$inputs, "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<VecmatOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$inputs,
            "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addTypes(resultTensorTypes);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<VecmatOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$operands,
            CArg<"ArrayRef<NamedAttribute>", "{}">:$attributes),
      [{
        $_state.addOperands(operands);
        $_state.addAttributes(attributes);
        $_state.addTypes(resultTensorTypes);
        (void)$_state.addRegion();
      }]>
      
    ];
    let printer = [{ return ::printNamedStructuredOp(p, *this); }];
    let parser = [{
      return ::parseNamedStructuredOp<VecmatOp>(parser, result);
    }];
    let hasFolder = 1;

    let extraClassDeclaration = structuredOpsBaseDecls # [{
      // Auto-generated.
      ArrayAttr iterator_types();
      ArrayAttr indexing_maps();
      static void regionBuilder(
        ImplicitLocOpBuilder &b, Block &block, ValueRange captures);
      static std::function<
        void(ImplicitLocOpBuilder &b, Block &, ValueRange)>
      getRegionBuilder() {
        return regionBuilder;
      }

      // Generic methods.
      static unsigned getNumRegionArgs();
      std::string getLibraryCallName();
      
    }];
}

//===----------------------------------------------------------------------===//
// Op definition for DotOp
//===----------------------------------------------------------------------===//

def DotOp : LinalgStructuredBase_Op<"dot", !listconcat([
  AttrSizedOperandSegments,
  DeclareOpInterfaceMethods<MemoryEffectsOpInterface>,
  SingleBlockImplicitTerminator<"YieldOp">],
  /*extraInterfaces=*/[LinalgContractionOpInterface])> {
    
  let summary = [{ Performs a dot product of two vectors to a scalar result. }];
  let description = [{
    Numeric casting is performed on the operands to the inner multiply, promoting
them to the same data type as the accumulator/output.
  }];

    let arguments = (ins
      Variadic<AnyType>:$inputs,
      Variadic<AnyShaped>:$outputs
    );
    let results = (outs Variadic<AnyRankedTensor>:$result_tensors);
    let regions = (region AnyRegion:$region);

    let skipDefaultBuilders = 1;
    let builders = [
      OpBuilder<
      (ins "ValueRange":$inputs, "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<DotOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$inputs,
            "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addTypes(resultTensorTypes);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<DotOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$operands,
            CArg<"ArrayRef<NamedAttribute>", "{}">:$attributes),
      [{
        $_state.addOperands(operands);
        $_state.addAttributes(attributes);
        $_state.addTypes(resultTensorTypes);
        (void)$_state.addRegion();
      }]>
      
    ];
    let printer = [{ return ::printNamedStructuredOp(p, *this); }];
    let parser = [{
      return ::parseNamedStructuredOp<DotOp>(parser, result);
    }];
    let hasFolder = 1;

    let extraClassDeclaration = structuredOpsBaseDecls # [{
      // Auto-generated.
      ArrayAttr iterator_types();
      ArrayAttr indexing_maps();
      static void regionBuilder(
        ImplicitLocOpBuilder &b, Block &block, ValueRange captures);
      static std::function<
        void(ImplicitLocOpBuilder &b, Block &, ValueRange)>
      getRegionBuilder() {
        return regionBuilder;
      }

      // Generic methods.
      static unsigned getNumRegionArgs();
      std::string getLibraryCallName();
      
    }];
}

//===----------------------------------------------------------------------===//
// Op definition for DepthwiseConv2DInputNhwcFilterHwcPolyOp
//===----------------------------------------------------------------------===//

def DepthwiseConv2DInputNhwcFilterHwcPolyOp : LinalgStructuredBase_Op<"depthwise_conv_2d_input_nhwc_filter_hwc_poly", !listconcat([
  AttrSizedOperandSegments,
  DeclareOpInterfaceMethods<MemoryEffectsOpInterface>,
  SingleBlockImplicitTerminator<"YieldOp">],
  /*extraInterfaces=*/[])> {
    
  let summary = [{ Performs depth-wise 2-D convolution. }];
  let description = [{
    Numeric casting is performed on the operands to the inner multiply, promoting
them to the same data type as the accumulator/output.
  }];

    let arguments = (ins
      Variadic<AnyType>:$inputs,
      Variadic<AnyShaped>:$outputs,
RankedI64ElementsAttr<[2]>:$strides,
RankedI64ElementsAttr<[2]>:$dilations
    );
    let results = (outs Variadic<AnyRankedTensor>:$result_tensors);
    let regions = (region AnyRegion:$region);

    let skipDefaultBuilders = 1;
    let builders = [
      OpBuilder<
      (ins "ValueRange":$inputs, "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<DepthwiseConv2DInputNhwcFilterHwcPolyOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$inputs,
            "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addTypes(resultTensorTypes);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<DepthwiseConv2DInputNhwcFilterHwcPolyOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$operands,
            CArg<"ArrayRef<NamedAttribute>", "{}">:$attributes),
      [{
        $_state.addOperands(operands);
        $_state.addAttributes(attributes);
        $_state.addTypes(resultTensorTypes);
        (void)$_state.addRegion();
      }]>
      
  , OpBuilder<
  (ins "TypeRange":$resultTensorTypes, "ValueRange":$inputs,
       "ValueRange":$outputs, "Attribute":$strides, "Attribute":$dilations),
  [{
    $_state.addOperands(inputs);
    $_state.addOperands(outputs);
    $_state.addTypes(resultTensorTypes);
    $_state.addAttribute(
      "operand_segment_sizes",
      $_builder.getI32VectorAttr({
        static_cast<int32_t>(inputs.size()),
        static_cast<int32_t>(outputs.size())}));
    createAndFillStructuredOpRegion<DepthwiseConv2DInputNhwcFilterHwcPolyOp>(
      $_builder,
      $_state,
      TypeRange(inputs),
      TypeRange(outputs));
    $_state.addAttribute("strides", strides);
$_state.addAttribute("dilations", dilations);
  }]>

    ];
    let printer = [{ return ::printNamedStructuredOp(p, *this); }];
    let parser = [{
      return ::parseNamedStructuredOp<DepthwiseConv2DInputNhwcFilterHwcPolyOp>(parser, result);
    }];
    let hasFolder = 1;

    let extraClassDeclaration = structuredOpsBaseDecls # [{
      // Auto-generated.
      ArrayAttr iterator_types();
      ArrayAttr indexing_maps();
      static void regionBuilder(
        ImplicitLocOpBuilder &b, Block &block, ValueRange captures);
      static std::function<
        void(ImplicitLocOpBuilder &b, Block &, ValueRange)>
      getRegionBuilder() {
        return regionBuilder;
      }

      // Generic methods.
      static unsigned getNumRegionArgs();
      std::string getLibraryCallName();
      
      bool hasDynamicIndexingMaps();
      LogicalResult verifyIndexingMapRequiredAttributes();
    
    }];
}

//===----------------------------------------------------------------------===//
// Op definition for PoolingNhwcSumPolyOp
//===----------------------------------------------------------------------===//

def PoolingNhwcSumPolyOp : LinalgStructuredBase_Op<"pooling_nhwc_sum_poly", !listconcat([
  AttrSizedOperandSegments,
  DeclareOpInterfaceMethods<MemoryEffectsOpInterface>,
  SingleBlockImplicitTerminator<"YieldOp">],
  /*extraInterfaces=*/[])> {
    
  let summary = [{ Performs sum pooling. }];
  let description = [{
    Numeric casting is performed on the input operand, promoting it to the same
data type as the accumulator/output.
  }];

    let arguments = (ins
      Variadic<AnyType>:$inputs,
      Variadic<AnyShaped>:$outputs,
RankedI64ElementsAttr<[2]>:$strides,
RankedI64ElementsAttr<[2]>:$dilations
    );
    let results = (outs Variadic<AnyRankedTensor>:$result_tensors);
    let regions = (region AnyRegion:$region);

    let skipDefaultBuilders = 1;
    let builders = [
      OpBuilder<
      (ins "ValueRange":$inputs, "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<PoolingNhwcSumPolyOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$inputs,
            "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addTypes(resultTensorTypes);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<PoolingNhwcSumPolyOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$operands,
            CArg<"ArrayRef<NamedAttribute>", "{}">:$attributes),
      [{
        $_state.addOperands(operands);
        $_state.addAttributes(attributes);
        $_state.addTypes(resultTensorTypes);
        (void)$_state.addRegion();
      }]>
      
  , OpBuilder<
  (ins "TypeRange":$resultTensorTypes, "ValueRange":$inputs,
       "ValueRange":$outputs, "Attribute":$strides, "Attribute":$dilations),
  [{
    $_state.addOperands(inputs);
    $_state.addOperands(outputs);
    $_state.addTypes(resultTensorTypes);
    $_state.addAttribute(
      "operand_segment_sizes",
      $_builder.getI32VectorAttr({
        static_cast<int32_t>(inputs.size()),
        static_cast<int32_t>(outputs.size())}));
    createAndFillStructuredOpRegion<PoolingNhwcSumPolyOp>(
      $_builder,
      $_state,
      TypeRange(inputs),
      TypeRange(outputs));
    $_state.addAttribute("strides", strides);
$_state.addAttribute("dilations", dilations);
  }]>

    ];
    let printer = [{ return ::printNamedStructuredOp(p, *this); }];
    let parser = [{
      return ::parseNamedStructuredOp<PoolingNhwcSumPolyOp>(parser, result);
    }];
    let hasFolder = 1;

    let extraClassDeclaration = structuredOpsBaseDecls # [{
      // Auto-generated.
      ArrayAttr iterator_types();
      ArrayAttr indexing_maps();
      static void regionBuilder(
        ImplicitLocOpBuilder &b, Block &block, ValueRange captures);
      static std::function<
        void(ImplicitLocOpBuilder &b, Block &, ValueRange)>
      getRegionBuilder() {
        return regionBuilder;
      }

      // Generic methods.
      static unsigned getNumRegionArgs();
      std::string getLibraryCallName();
      
      bool hasDynamicIndexingMaps();
      LogicalResult verifyIndexingMapRequiredAttributes();
    
    }];
}

//===----------------------------------------------------------------------===//
// Op definition for FillRng2DOp
//===----------------------------------------------------------------------===//

def FillRng2DOp : LinalgStructuredBase_Op<"fill_rng_2d", !listconcat([
  AttrSizedOperandSegments,
  DeclareOpInterfaceMethods<MemoryEffectsOpInterface>,
  SingleBlockImplicitTerminator<"YieldOp">],
  /*extraInterfaces=*/[])> {
    
  let summary = [{ Fills the output tensor with pseudo random numbers. }];
  let description = [{
    The operation generations pseudo random numbers using a linear congruential
generator. It provides no guarantees regarding the distribution of the
generated random numbers. Instead of generating the random numbers
sequentially, it instantiates one random number generator per data element
and runs them in parallel. The seed operand and the indices of the data
element seed the random number generation. The min and max operands limit
the range of the generated random numbers.
  }];

    let arguments = (ins
      Variadic<AnyType>:$inputs,
      Variadic<AnyShaped>:$outputs
    );
    let results = (outs Variadic<AnyRankedTensor>:$result_tensors);
    let regions = (region AnyRegion:$region);

    let skipDefaultBuilders = 1;
    let builders = [
      OpBuilder<
      (ins "ValueRange":$inputs, "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<FillRng2DOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$inputs,
            "ValueRange":$outputs),
      [{
        $_state.addOperands(inputs);
        $_state.addOperands(outputs);
        $_state.addTypes(resultTensorTypes);
        $_state.addAttribute(
          "operand_segment_sizes",
          $_builder.getI32VectorAttr({
            static_cast<int32_t>(inputs.size()),
            static_cast<int32_t>(outputs.size())}));
        createAndFillStructuredOpRegion<FillRng2DOp>(
          $_builder,
          $_state,
          TypeRange(inputs),
          TypeRange(outputs));
      }]>,
      OpBuilder<
      (ins "TypeRange":$resultTensorTypes, "ValueRange":$operands,
            CArg<"ArrayRef<NamedAttribute>", "{}">:$attributes),
      [{
        $_state.addOperands(operands);
        $_state.addAttributes(attributes);
        $_state.addTypes(resultTensorTypes);
        (void)$_state.addRegion();
      }]>
      
    ];
    let printer = [{ return ::printNamedStructuredOp(p, *this); }];
    let parser = [{
      return ::parseNamedStructuredOp<FillRng2DOp>(parser, result);
    }];
    let hasFolder = 1;

    let extraClassDeclaration = structuredOpsBaseDecls # [{
      // Auto-generated.
      ArrayAttr iterator_types();
      ArrayAttr indexing_maps();
      static void regionBuilder(
        ImplicitLocOpBuilder &b, Block &block, ValueRange captures);
      static std::function<
        void(ImplicitLocOpBuilder &b, Block &, ValueRange)>
      getRegionBuilder() {
        return regionBuilder;
      }

      // Generic methods.
      static unsigned getNumRegionArgs();
      std::string getLibraryCallName();
      
    }];
}
