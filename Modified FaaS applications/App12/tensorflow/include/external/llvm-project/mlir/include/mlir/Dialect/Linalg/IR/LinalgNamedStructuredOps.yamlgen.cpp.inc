
//===----------------------------------------------------------------------===//
// Implementation of MatmulOp
//===----------------------------------------------------------------------===//

ArrayAttr MatmulOp::iterator_types() {
  return Builder(getContext()).getStrArrayAttr(SmallVector<StringRef>{ getParallelIteratorTypeName(), getParallelIteratorTypeName(), getReductionIteratorTypeName() });
}

static SmallVector<AffineExpr> getSymbolBindings(MatmulOp self) {
  MLIRContext *context = self.getContext();
  SmallVector<AffineExpr> exprs;
  exprs.push_back(getAffineSymbolExpr(0, context));
  exprs.push_back(getAffineSymbolExpr(1, context));
  exprs.push_back(getAffineSymbolExpr(2, context));
  return exprs;
}

ArrayAttr MatmulOp::indexing_maps() {
  static const char memoizeAttr[] = "linalg.memoized_indexing_maps";
  ArrayAttr cached = getOperation()->getAttrOfType<ArrayAttr>(memoizeAttr);
  if (cached)
    return cached;

  MLIRContext *context = getContext();
  auto symbolBindings = getSymbolBindings(*this);
  SmallVector<AffineMap> maps;
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2)[s0, s1, s2] -> (d0, d2)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 3, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2)[s0, s1, s2] -> (d2, d1)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 3, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2)[s0, s1, s2] -> (d0, d1)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 3, 0));
  cached = Builder(context).getAffineMapArrayAttr(maps);
  getOperation()->setAttr(memoizeAttr, cached);
  return cached;
}

unsigned MatmulOp::getNumRegionArgs() { return 3; }

std::string MatmulOp::getLibraryCallName() {
  return generateLibraryCallName(getOperation());
}

void MatmulOp::regionBuilder(
    ImplicitLocOpBuilder &b, Block &block, ValueRange captures) {
  assert(3 > 0 && block.getNumArguments() == 3 &&
         "MatmulOp regionBuilder expects 3 (>=0) args");
  RegionBuilderHelper helper(block.getArgument(0).getContext(), block);
  SmallVector<Value> yields;
  Value value1 = helper.cast(block.getArgument(2).getType(), block.getArgument(0));
  Value value2 = helper.cast(block.getArgument(2).getType(), block.getArgument(1));
  Value value3 = helper.applyfn__mul(value1, value2);
  Value value4 = helper.applyfn__add(block.getArgument(2), value3);
  yields.push_back(value4);
  helper.yieldOutputs(yields);
}

LogicalResult MatmulOp::fold(ArrayRef<Attribute>,
                        SmallVectorImpl<OpFoldResult> &) {
  return foldMemRefCast(*this);
}
void MatmulOp::getEffects(SmallVectorImpl<
    SideEffects::EffectInstance<MemoryEffects::Effect> >&effects) {
      SmallVector<Value> inputBuffers = getInputBufferOperands();
      SmallVector<Value> outputBuffers = getOutputBufferOperands();
      getGenericEffectsImpl(effects,
        getOperation()->getResults(), inputBuffers, outputBuffers);
}

//===----------------------------------------------------------------------===//
// Implementation of BatchMatmulOp
//===----------------------------------------------------------------------===//

ArrayAttr BatchMatmulOp::iterator_types() {
  return Builder(getContext()).getStrArrayAttr(SmallVector<StringRef>{ getParallelIteratorTypeName(), getParallelIteratorTypeName(), getParallelIteratorTypeName(), getReductionIteratorTypeName() });
}

static SmallVector<AffineExpr> getSymbolBindings(BatchMatmulOp self) {
  MLIRContext *context = self.getContext();
  SmallVector<AffineExpr> exprs;
  exprs.push_back(getAffineSymbolExpr(0, context));
  exprs.push_back(getAffineSymbolExpr(1, context));
  exprs.push_back(getAffineSymbolExpr(2, context));
  exprs.push_back(getAffineSymbolExpr(3, context));
  return exprs;
}

ArrayAttr BatchMatmulOp::indexing_maps() {
  static const char memoizeAttr[] = "linalg.memoized_indexing_maps";
  ArrayAttr cached = getOperation()->getAttrOfType<ArrayAttr>(memoizeAttr);
  if (cached)
    return cached;

  MLIRContext *context = getContext();
  auto symbolBindings = getSymbolBindings(*this);
  SmallVector<AffineMap> maps;
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2, d3)[s0, s1, s2, s3] -> (d0, d1, d3)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 4, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2, d3)[s0, s1, s2, s3] -> (d0, d3, d2)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 4, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2, d3)[s0, s1, s2, s3] -> (d0, d1, d2)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 4, 0));
  cached = Builder(context).getAffineMapArrayAttr(maps);
  getOperation()->setAttr(memoizeAttr, cached);
  return cached;
}

unsigned BatchMatmulOp::getNumRegionArgs() { return 3; }

std::string BatchMatmulOp::getLibraryCallName() {
  return generateLibraryCallName(getOperation());
}

void BatchMatmulOp::regionBuilder(
    ImplicitLocOpBuilder &b, Block &block, ValueRange captures) {
  assert(3 > 0 && block.getNumArguments() == 3 &&
         "BatchMatmulOp regionBuilder expects 3 (>=0) args");
  RegionBuilderHelper helper(block.getArgument(0).getContext(), block);
  SmallVector<Value> yields;
  Value value1 = helper.cast(block.getArgument(2).getType(), block.getArgument(0));
  Value value2 = helper.cast(block.getArgument(2).getType(), block.getArgument(1));
  Value value3 = helper.applyfn__mul(value1, value2);
  Value value4 = helper.applyfn__add(block.getArgument(2), value3);
  yields.push_back(value4);
  helper.yieldOutputs(yields);
}

LogicalResult BatchMatmulOp::fold(ArrayRef<Attribute>,
                        SmallVectorImpl<OpFoldResult> &) {
  return foldMemRefCast(*this);
}
void BatchMatmulOp::getEffects(SmallVectorImpl<
    SideEffects::EffectInstance<MemoryEffects::Effect> >&effects) {
      SmallVector<Value> inputBuffers = getInputBufferOperands();
      SmallVector<Value> outputBuffers = getOutputBufferOperands();
      getGenericEffectsImpl(effects,
        getOperation()->getResults(), inputBuffers, outputBuffers);
}

//===----------------------------------------------------------------------===//
// Implementation of MatvecOp
//===----------------------------------------------------------------------===//

ArrayAttr MatvecOp::iterator_types() {
  return Builder(getContext()).getStrArrayAttr(SmallVector<StringRef>{ getParallelIteratorTypeName(), getReductionIteratorTypeName() });
}

static SmallVector<AffineExpr> getSymbolBindings(MatvecOp self) {
  MLIRContext *context = self.getContext();
  SmallVector<AffineExpr> exprs;
  exprs.push_back(getAffineSymbolExpr(0, context));
  exprs.push_back(getAffineSymbolExpr(1, context));
  return exprs;
}

ArrayAttr MatvecOp::indexing_maps() {
  static const char memoizeAttr[] = "linalg.memoized_indexing_maps";
  ArrayAttr cached = getOperation()->getAttrOfType<ArrayAttr>(memoizeAttr);
  if (cached)
    return cached;

  MLIRContext *context = getContext();
  auto symbolBindings = getSymbolBindings(*this);
  SmallVector<AffineMap> maps;
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1)[s0, s1] -> (d0, d1)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 2, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1)[s0, s1] -> (d1)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 2, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1)[s0, s1] -> (d0)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 2, 0));
  cached = Builder(context).getAffineMapArrayAttr(maps);
  getOperation()->setAttr(memoizeAttr, cached);
  return cached;
}

unsigned MatvecOp::getNumRegionArgs() { return 3; }

std::string MatvecOp::getLibraryCallName() {
  return generateLibraryCallName(getOperation());
}

void MatvecOp::regionBuilder(
    ImplicitLocOpBuilder &b, Block &block, ValueRange captures) {
  assert(3 > 0 && block.getNumArguments() == 3 &&
         "MatvecOp regionBuilder expects 3 (>=0) args");
  RegionBuilderHelper helper(block.getArgument(0).getContext(), block);
  SmallVector<Value> yields;
  Value value1 = helper.cast(block.getArgument(2).getType(), block.getArgument(0));
  Value value2 = helper.cast(block.getArgument(2).getType(), block.getArgument(1));
  Value value3 = helper.applyfn__mul(value1, value2);
  Value value4 = helper.applyfn__add(block.getArgument(2), value3);
  yields.push_back(value4);
  helper.yieldOutputs(yields);
}

LogicalResult MatvecOp::fold(ArrayRef<Attribute>,
                        SmallVectorImpl<OpFoldResult> &) {
  return foldMemRefCast(*this);
}
void MatvecOp::getEffects(SmallVectorImpl<
    SideEffects::EffectInstance<MemoryEffects::Effect> >&effects) {
      SmallVector<Value> inputBuffers = getInputBufferOperands();
      SmallVector<Value> outputBuffers = getOutputBufferOperands();
      getGenericEffectsImpl(effects,
        getOperation()->getResults(), inputBuffers, outputBuffers);
}

//===----------------------------------------------------------------------===//
// Implementation of VecmatOp
//===----------------------------------------------------------------------===//

ArrayAttr VecmatOp::iterator_types() {
  return Builder(getContext()).getStrArrayAttr(SmallVector<StringRef>{ getParallelIteratorTypeName(), getReductionIteratorTypeName() });
}

static SmallVector<AffineExpr> getSymbolBindings(VecmatOp self) {
  MLIRContext *context = self.getContext();
  SmallVector<AffineExpr> exprs;
  exprs.push_back(getAffineSymbolExpr(0, context));
  exprs.push_back(getAffineSymbolExpr(1, context));
  return exprs;
}

ArrayAttr VecmatOp::indexing_maps() {
  static const char memoizeAttr[] = "linalg.memoized_indexing_maps";
  ArrayAttr cached = getOperation()->getAttrOfType<ArrayAttr>(memoizeAttr);
  if (cached)
    return cached;

  MLIRContext *context = getContext();
  auto symbolBindings = getSymbolBindings(*this);
  SmallVector<AffineMap> maps;
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1)[s0, s1] -> (d1)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 2, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1)[s0, s1] -> (d1, d0)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 2, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1)[s0, s1] -> (d0)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 2, 0));
  cached = Builder(context).getAffineMapArrayAttr(maps);
  getOperation()->setAttr(memoizeAttr, cached);
  return cached;
}

unsigned VecmatOp::getNumRegionArgs() { return 3; }

std::string VecmatOp::getLibraryCallName() {
  return generateLibraryCallName(getOperation());
}

void VecmatOp::regionBuilder(
    ImplicitLocOpBuilder &b, Block &block, ValueRange captures) {
  assert(3 > 0 && block.getNumArguments() == 3 &&
         "VecmatOp regionBuilder expects 3 (>=0) args");
  RegionBuilderHelper helper(block.getArgument(0).getContext(), block);
  SmallVector<Value> yields;
  Value value1 = helper.cast(block.getArgument(2).getType(), block.getArgument(0));
  Value value2 = helper.cast(block.getArgument(2).getType(), block.getArgument(1));
  Value value3 = helper.applyfn__mul(value1, value2);
  Value value4 = helper.applyfn__add(block.getArgument(2), value3);
  yields.push_back(value4);
  helper.yieldOutputs(yields);
}

LogicalResult VecmatOp::fold(ArrayRef<Attribute>,
                        SmallVectorImpl<OpFoldResult> &) {
  return foldMemRefCast(*this);
}
void VecmatOp::getEffects(SmallVectorImpl<
    SideEffects::EffectInstance<MemoryEffects::Effect> >&effects) {
      SmallVector<Value> inputBuffers = getInputBufferOperands();
      SmallVector<Value> outputBuffers = getOutputBufferOperands();
      getGenericEffectsImpl(effects,
        getOperation()->getResults(), inputBuffers, outputBuffers);
}

//===----------------------------------------------------------------------===//
// Implementation of DotOp
//===----------------------------------------------------------------------===//

ArrayAttr DotOp::iterator_types() {
  return Builder(getContext()).getStrArrayAttr(SmallVector<StringRef>{ getReductionIteratorTypeName() });
}

static SmallVector<AffineExpr> getSymbolBindings(DotOp self) {
  MLIRContext *context = self.getContext();
  SmallVector<AffineExpr> exprs;
  exprs.push_back(getAffineSymbolExpr(0, context));
  return exprs;
}

ArrayAttr DotOp::indexing_maps() {
  static const char memoizeAttr[] = "linalg.memoized_indexing_maps";
  ArrayAttr cached = getOperation()->getAttrOfType<ArrayAttr>(memoizeAttr);
  if (cached)
    return cached;

  MLIRContext *context = getContext();
  auto symbolBindings = getSymbolBindings(*this);
  SmallVector<AffineMap> maps;
  maps.push_back(mlir::parseAttribute("affine_map<(d0)[s0] -> (d0)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 1, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0)[s0] -> (d0)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 1, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0)[s0] -> ()>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 1, 0));
  cached = Builder(context).getAffineMapArrayAttr(maps);
  getOperation()->setAttr(memoizeAttr, cached);
  return cached;
}

unsigned DotOp::getNumRegionArgs() { return 3; }

std::string DotOp::getLibraryCallName() {
  return generateLibraryCallName(getOperation());
}

void DotOp::regionBuilder(
    ImplicitLocOpBuilder &b, Block &block, ValueRange captures) {
  assert(3 > 0 && block.getNumArguments() == 3 &&
         "DotOp regionBuilder expects 3 (>=0) args");
  RegionBuilderHelper helper(block.getArgument(0).getContext(), block);
  SmallVector<Value> yields;
  Value value1 = helper.cast(block.getArgument(2).getType(), block.getArgument(0));
  Value value2 = helper.cast(block.getArgument(2).getType(), block.getArgument(1));
  Value value3 = helper.applyfn__mul(value1, value2);
  Value value4 = helper.applyfn__add(block.getArgument(2), value3);
  yields.push_back(value4);
  helper.yieldOutputs(yields);
}

LogicalResult DotOp::fold(ArrayRef<Attribute>,
                        SmallVectorImpl<OpFoldResult> &) {
  return foldMemRefCast(*this);
}
void DotOp::getEffects(SmallVectorImpl<
    SideEffects::EffectInstance<MemoryEffects::Effect> >&effects) {
      SmallVector<Value> inputBuffers = getInputBufferOperands();
      SmallVector<Value> outputBuffers = getOutputBufferOperands();
      getGenericEffectsImpl(effects,
        getOperation()->getResults(), inputBuffers, outputBuffers);
}

//===----------------------------------------------------------------------===//
// Implementation of DepthwiseConv2DInputNhwcFilterHwcPolyOp
//===----------------------------------------------------------------------===//

ArrayAttr DepthwiseConv2DInputNhwcFilterHwcPolyOp::iterator_types() {
  return Builder(getContext()).getStrArrayAttr(SmallVector<StringRef>{ getParallelIteratorTypeName(), getParallelIteratorTypeName(), getParallelIteratorTypeName(), getParallelIteratorTypeName(), getReductionIteratorTypeName(), getReductionIteratorTypeName() });
}

static SmallVector<AffineExpr> getSymbolBindings(DepthwiseConv2DInputNhwcFilterHwcPolyOp self) {
  MLIRContext *context = self.getContext();
  SmallVector<AffineExpr> exprs;
  exprs.push_back(getAffineSymbolExpr(0, context));
  exprs.push_back(getAffineSymbolExpr(1, context));
  exprs.push_back(getAffineSymbolExpr(2, context));
  exprs.push_back(getAffineSymbolExpr(3, context));
  exprs.push_back(getAffineSymbolExpr(4, context));
  exprs.push_back(getAffineSymbolExpr(5, context));
  exprs.push_back(getAffineSymbolExpr(6, context));
  exprs.push_back(getAffineSymbolExpr(7, context));

int64_t cst8 = self.strides().getValue<int64_t>({ 0 });
exprs.push_back(getAffineConstantExpr(cst8, context));


int64_t cst9 = self.strides().getValue<int64_t>({ 1 });
exprs.push_back(getAffineConstantExpr(cst9, context));


int64_t cst10 = self.dilations().getValue<int64_t>({ 0 });
exprs.push_back(getAffineConstantExpr(cst10, context));


int64_t cst11 = self.dilations().getValue<int64_t>({ 1 });
exprs.push_back(getAffineConstantExpr(cst11, context));

  return exprs;
}

ArrayAttr DepthwiseConv2DInputNhwcFilterHwcPolyOp::indexing_maps() {
  static const char memoizeAttr[] = "linalg.memoized_indexing_maps";
  ArrayAttr cached = getOperation()->getAttrOfType<ArrayAttr>(memoizeAttr);
  if (cached)
    return cached;

  MLIRContext *context = getContext();
  auto symbolBindings = getSymbolBindings(*this);
  SmallVector<AffineMap> maps;
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2, d3, d4, d5)[s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11] -> (d0, d1 * s8 + d4 * s10, d2 * s9 + d5 * s11, d3)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 6, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2, d3, d4, d5)[s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11] -> (d4, d5, d3)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 6, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2, d3, d4, d5)[s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11] -> (d0, d1, d2, d3)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 6, 0));
  cached = Builder(context).getAffineMapArrayAttr(maps);
  getOperation()->setAttr(memoizeAttr, cached);
  return cached;
}

unsigned DepthwiseConv2DInputNhwcFilterHwcPolyOp::getNumRegionArgs() { return 3; }

std::string DepthwiseConv2DInputNhwcFilterHwcPolyOp::getLibraryCallName() {
  return generateLibraryCallName(getOperation());
}

bool DepthwiseConv2DInputNhwcFilterHwcPolyOp::hasDynamicIndexingMaps() { return true; }
LogicalResult DepthwiseConv2DInputNhwcFilterHwcPolyOp::verifyIndexingMapRequiredAttributes() {
  Operation *op = getOperation();
  
if (auto attr = op->getAttrOfType<DenseElementsAttr>("strides")) {
  if (!attr.getType().getElementType().isInteger(64))
    return op->emitError(
      "incorrect element type for indexing map required attribute 'strides'");
  if (attr.getType().getShape() != ArrayRef<int64_t>{ 2 })
    return op->emitError(
      "incorrect shape for indexing map required attribute 'strides'");
} else {
  return op->emitError(
    "missing indexing map required attribute 'strides'");
}


if (auto attr = op->getAttrOfType<DenseElementsAttr>("dilations")) {
  if (!attr.getType().getElementType().isInteger(64))
    return op->emitError(
      "incorrect element type for indexing map required attribute 'dilations'");
  if (attr.getType().getShape() != ArrayRef<int64_t>{ 2 })
    return op->emitError(
      "incorrect shape for indexing map required attribute 'dilations'");
} else {
  return op->emitError(
    "missing indexing map required attribute 'dilations'");
}

  return success();
}

void DepthwiseConv2DInputNhwcFilterHwcPolyOp::regionBuilder(
    ImplicitLocOpBuilder &b, Block &block, ValueRange captures) {
  assert(3 > 0 && block.getNumArguments() == 3 &&
         "DepthwiseConv2DInputNhwcFilterHwcPolyOp regionBuilder expects 3 (>=0) args");
  RegionBuilderHelper helper(block.getArgument(0).getContext(), block);
  SmallVector<Value> yields;
  Value value1 = helper.cast(block.getArgument(2).getType(), block.getArgument(0));
  Value value2 = helper.cast(block.getArgument(2).getType(), block.getArgument(1));
  Value value3 = helper.applyfn__mul(value1, value2);
  Value value4 = helper.applyfn__add(block.getArgument(2), value3);
  yields.push_back(value4);
  helper.yieldOutputs(yields);
}

LogicalResult DepthwiseConv2DInputNhwcFilterHwcPolyOp::fold(ArrayRef<Attribute>,
                        SmallVectorImpl<OpFoldResult> &) {
  return foldMemRefCast(*this);
}
void DepthwiseConv2DInputNhwcFilterHwcPolyOp::getEffects(SmallVectorImpl<
    SideEffects::EffectInstance<MemoryEffects::Effect> >&effects) {
      SmallVector<Value> inputBuffers = getInputBufferOperands();
      SmallVector<Value> outputBuffers = getOutputBufferOperands();
      getGenericEffectsImpl(effects,
        getOperation()->getResults(), inputBuffers, outputBuffers);
}

//===----------------------------------------------------------------------===//
// Implementation of PoolingNhwcSumPolyOp
//===----------------------------------------------------------------------===//

ArrayAttr PoolingNhwcSumPolyOp::iterator_types() {
  return Builder(getContext()).getStrArrayAttr(SmallVector<StringRef>{ getReductionIteratorTypeName(), getReductionIteratorTypeName(), getParallelIteratorTypeName(), getParallelIteratorTypeName(), getParallelIteratorTypeName(), getParallelIteratorTypeName() });
}

static SmallVector<AffineExpr> getSymbolBindings(PoolingNhwcSumPolyOp self) {
  MLIRContext *context = self.getContext();
  SmallVector<AffineExpr> exprs;
  exprs.push_back(getAffineSymbolExpr(0, context));
  exprs.push_back(getAffineSymbolExpr(1, context));
  exprs.push_back(getAffineSymbolExpr(2, context));
  exprs.push_back(getAffineSymbolExpr(3, context));
  exprs.push_back(getAffineSymbolExpr(4, context));
  exprs.push_back(getAffineSymbolExpr(5, context));

int64_t cst6 = self.strides().getValue<int64_t>({ 0 });
exprs.push_back(getAffineConstantExpr(cst6, context));


int64_t cst7 = self.strides().getValue<int64_t>({ 1 });
exprs.push_back(getAffineConstantExpr(cst7, context));


int64_t cst8 = self.dilations().getValue<int64_t>({ 0 });
exprs.push_back(getAffineConstantExpr(cst8, context));


int64_t cst9 = self.dilations().getValue<int64_t>({ 1 });
exprs.push_back(getAffineConstantExpr(cst9, context));

  exprs.push_back(getAffineSymbolExpr(10, context));
  exprs.push_back(getAffineSymbolExpr(11, context));
  return exprs;
}

ArrayAttr PoolingNhwcSumPolyOp::indexing_maps() {
  static const char memoizeAttr[] = "linalg.memoized_indexing_maps";
  ArrayAttr cached = getOperation()->getAttrOfType<ArrayAttr>(memoizeAttr);
  if (cached)
    return cached;

  MLIRContext *context = getContext();
  auto symbolBindings = getSymbolBindings(*this);
  SmallVector<AffineMap> maps;
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2, d3, d4, d5)[s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11] -> (d2, d3 * s6 + d0 * s8, d4 * s7 + d1 * s9, d5)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 6, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2, d3, d4, d5)[s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11] -> (d0, d1)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 6, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1, d2, d3, d4, d5)[s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11] -> (d2, d3, d4, d5)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 6, 0));
  cached = Builder(context).getAffineMapArrayAttr(maps);
  getOperation()->setAttr(memoizeAttr, cached);
  return cached;
}

unsigned PoolingNhwcSumPolyOp::getNumRegionArgs() { return 3; }

std::string PoolingNhwcSumPolyOp::getLibraryCallName() {
  return generateLibraryCallName(getOperation());
}

bool PoolingNhwcSumPolyOp::hasDynamicIndexingMaps() { return true; }
LogicalResult PoolingNhwcSumPolyOp::verifyIndexingMapRequiredAttributes() {
  Operation *op = getOperation();
  
if (auto attr = op->getAttrOfType<DenseElementsAttr>("strides")) {
  if (!attr.getType().getElementType().isInteger(64))
    return op->emitError(
      "incorrect element type for indexing map required attribute 'strides'");
  if (attr.getType().getShape() != ArrayRef<int64_t>{ 2 })
    return op->emitError(
      "incorrect shape for indexing map required attribute 'strides'");
} else {
  return op->emitError(
    "missing indexing map required attribute 'strides'");
}


if (auto attr = op->getAttrOfType<DenseElementsAttr>("dilations")) {
  if (!attr.getType().getElementType().isInteger(64))
    return op->emitError(
      "incorrect element type for indexing map required attribute 'dilations'");
  if (attr.getType().getShape() != ArrayRef<int64_t>{ 2 })
    return op->emitError(
      "incorrect shape for indexing map required attribute 'dilations'");
} else {
  return op->emitError(
    "missing indexing map required attribute 'dilations'");
}

  return success();
}

void PoolingNhwcSumPolyOp::regionBuilder(
    ImplicitLocOpBuilder &b, Block &block, ValueRange captures) {
  assert(3 > 0 && block.getNumArguments() == 3 &&
         "PoolingNhwcSumPolyOp regionBuilder expects 3 (>=0) args");
  RegionBuilderHelper helper(block.getArgument(0).getContext(), block);
  SmallVector<Value> yields;
  Value value1 = helper.cast(block.getArgument(2).getType(), block.getArgument(0));
  Value value2 = helper.applyfn__add(block.getArgument(2), value1);
  yields.push_back(value2);
  helper.yieldOutputs(yields);
}

LogicalResult PoolingNhwcSumPolyOp::fold(ArrayRef<Attribute>,
                        SmallVectorImpl<OpFoldResult> &) {
  return foldMemRefCast(*this);
}
void PoolingNhwcSumPolyOp::getEffects(SmallVectorImpl<
    SideEffects::EffectInstance<MemoryEffects::Effect> >&effects) {
      SmallVector<Value> inputBuffers = getInputBufferOperands();
      SmallVector<Value> outputBuffers = getOutputBufferOperands();
      getGenericEffectsImpl(effects,
        getOperation()->getResults(), inputBuffers, outputBuffers);
}

//===----------------------------------------------------------------------===//
// Implementation of FillRng2DOp
//===----------------------------------------------------------------------===//

ArrayAttr FillRng2DOp::iterator_types() {
  return Builder(getContext()).getStrArrayAttr(SmallVector<StringRef>{ getParallelIteratorTypeName(), getParallelIteratorTypeName() });
}

static SmallVector<AffineExpr> getSymbolBindings(FillRng2DOp self) {
  MLIRContext *context = self.getContext();
  SmallVector<AffineExpr> exprs;
  exprs.push_back(getAffineSymbolExpr(0, context));
  exprs.push_back(getAffineSymbolExpr(1, context));
  return exprs;
}

ArrayAttr FillRng2DOp::indexing_maps() {
  static const char memoizeAttr[] = "linalg.memoized_indexing_maps";
  ArrayAttr cached = getOperation()->getAttrOfType<ArrayAttr>(memoizeAttr);
  if (cached)
    return cached;

  MLIRContext *context = getContext();
  auto symbolBindings = getSymbolBindings(*this);
  SmallVector<AffineMap> maps;
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1)[s0, s1] -> ()>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 2, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1)[s0, s1] -> ()>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 2, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1)[s0, s1] -> ()>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 2, 0));
  maps.push_back(mlir::parseAttribute("affine_map<(d0, d1)[s0, s1] -> (d0, d1)>", context).cast<AffineMapAttr>().getValue());
  maps.back() = simplifyAffineMap(maps.back().replaceDimsAndSymbols({}, symbolBindings, 2, 0));
  cached = Builder(context).getAffineMapArrayAttr(maps);
  getOperation()->setAttr(memoizeAttr, cached);
  return cached;
}

unsigned FillRng2DOp::getNumRegionArgs() { return 4; }

std::string FillRng2DOp::getLibraryCallName() {
  return generateLibraryCallName(getOperation());
}

void FillRng2DOp::regionBuilder(
    ImplicitLocOpBuilder &b, Block &block, ValueRange captures) {
  assert(4 > 0 && block.getNumArguments() == 4 &&
         "FillRng2DOp regionBuilder expects 4 (>=0) args");
  RegionBuilderHelper helper(block.getArgument(0).getContext(), block);
  SmallVector<Value> yields;
  Value value1 = helper.constant("2147483647 : i64");
  Value value2 = helper.cast(helper.getFloat64Type(), value1);
  Value value3 = helper.index(1);
  Value value4 = helper.cast(helper.getIntegerType(32), value3);
  Value value5 = helper.index(0);
  Value value6 = helper.cast(helper.getIntegerType(32), value5);
  Value value7 = helper.applyfn__add(value6, block.getArgument(2));
  Value value8 = helper.constant("1103515245 : i64");
  Value value9 = helper.cast(helper.getIntegerType(32), value8);
  Value value10 = helper.applyfn__mul(value7, value9);
  Value value11 = helper.constant("12345 : i64");
  Value value12 = helper.cast(helper.getIntegerType(32), value11);
  Value value13 = helper.applyfn__add(value10, value12);
  Value value14 = helper.applyfn__add(value4, value13);
  Value value15 = helper.constant("1103515245 : i64");
  Value value16 = helper.cast(helper.getIntegerType(32), value15);
  Value value17 = helper.applyfn__mul(value14, value16);
  Value value18 = helper.constant("12345 : i64");
  Value value19 = helper.cast(helper.getIntegerType(32), value18);
  Value value20 = helper.applyfn__add(value17, value19);
  Value value21 = helper.cast(helper.getFloat64Type(), value20);
  Value value22 = helper.applyfn__add(value2, value21);
  Value value23 = helper.applyfn__sub(block.getArgument(1), block.getArgument(0));
  Value value24 = helper.constant("2.3283063999999999E-10 : f64");
  Value value25 = helper.cast(helper.getFloat64Type(), value24);
  Value value26 = helper.applyfn__mul(value23, value25);
  Value value27 = helper.applyfn__mul(value22, value26);
  Value value28 = helper.applyfn__add(value27, block.getArgument(0));
  Value value29 = helper.cast(block.getArgument(3).getType(), value28);
  yields.push_back(value29);
  helper.yieldOutputs(yields);
}

LogicalResult FillRng2DOp::fold(ArrayRef<Attribute>,
                        SmallVectorImpl<OpFoldResult> &) {
  return foldMemRefCast(*this);
}
void FillRng2DOp::getEffects(SmallVectorImpl<
    SideEffects::EffectInstance<MemoryEffects::Effect> >&effects) {
      SmallVector<Value> inputBuffers = getInputBufferOperands();
      SmallVector<Value> outputBuffers = getOutputBufferOperands();
      getGenericEffectsImpl(effects,
        getOperation()->getResults(), inputBuffers, outputBuffers);
}
