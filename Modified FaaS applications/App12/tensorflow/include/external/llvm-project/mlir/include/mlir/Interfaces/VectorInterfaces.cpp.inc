/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

StringRef mlir::VectorTransferOpInterface::getInBoundsAttrName() {
      return getImpl()->getInBoundsAttrName();
  }
StringRef mlir::VectorTransferOpInterface::getPermutationMapAttrName() {
      return getImpl()->getPermutationMapAttrName();
  }
bool mlir::VectorTransferOpInterface::isDimInBounds(unsigned dim) {
      return getImpl()->isDimInBounds(getImpl(), getOperation(), dim);
  }
Value mlir::VectorTransferOpInterface::source() {
      return getImpl()->source(getImpl(), getOperation());
  }
Value mlir::VectorTransferOpInterface::vector() {
      return getImpl()->vector(getImpl(), getOperation());
  }
ValueRange mlir::VectorTransferOpInterface::indices() {
      return getImpl()->indices(getImpl(), getOperation());
  }
AffineMap mlir::VectorTransferOpInterface::permutation_map() {
      return getImpl()->permutation_map(getImpl(), getOperation());
  }
bool mlir::VectorTransferOpInterface::isBroadcastDim(unsigned idx) {
      return getImpl()->isBroadcastDim(getImpl(), getOperation(), idx);
  }
bool mlir::VectorTransferOpInterface::hasBroadcastDim() {
      return getImpl()->hasBroadcastDim(getImpl(), getOperation());
  }
Optional<ArrayAttr> mlir::VectorTransferOpInterface::in_bounds() {
      return getImpl()->in_bounds(getImpl(), getOperation());
  }
ShapedType mlir::VectorTransferOpInterface::getShapedType() {
      return getImpl()->getShapedType(getImpl(), getOperation());
  }
VectorType mlir::VectorTransferOpInterface::getVectorType() {
      return getImpl()->getVectorType(getImpl(), getOperation());
  }
VectorType mlir::VectorTransferOpInterface::getMaskType() {
      return getImpl()->getMaskType(getImpl(), getOperation());
  }
unsigned mlir::VectorTransferOpInterface::getTransferRank() {
      return getImpl()->getTransferRank(getImpl(), getOperation());
  }
unsigned mlir::VectorTransferOpInterface::getLeadingShapedRank() {
      return getImpl()->getLeadingShapedRank(getImpl(), getOperation());
  }
bool mlir::VectorTransferOpInterface::hasOutOfBoundsDim() {
      return getImpl()->hasOutOfBoundsDim(getImpl(), getOperation());
  }
void mlir::VectorTransferOpInterface::zipResultAndIndexing(llvm::function_ref<void(int64_t, int64_t)> fun) {
      return getImpl()->zipResultAndIndexing(getImpl(), getOperation(), fun);
  }
Optional<SmallVector<int64_t, 4>> mlir::VectorUnrollOpInterface::getShapeForUnroll() {
      return getImpl()->getShapeForUnroll(getImpl(), getOperation());
  }
