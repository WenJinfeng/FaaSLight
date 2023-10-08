/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Declarations                                                            *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#if defined(GET_OP_CLASSES) || defined(GET_OP_FWD_DEFINES)
#undef GET_OP_FWD_DEFINES
namespace mlir {
namespace TF {
class _JitFusedMatMulOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _TfrtGetResourceOp;
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {
class _TfrtSetResourceOp;
} // namespace TF
} // namespace mlir
#endif

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES

namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_JitFusedMatMulOp declarations
//===----------------------------------------------------------------------===//

class _JitFusedMatMulOpAdaptor {
public:
  _JitFusedMatMulOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});
  _JitFusedMatMulOpAdaptor(_JitFusedMatMulOp&op);
  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value a();
  ::mlir::Value b();
  ::mlir::ValueRange additional_args();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::BoolAttr transpose_a();
  ::mlir::BoolAttr transpose_b();
  ::mlir::ArrayAttr fusion();
  ::mlir::LogicalResult verify(::mlir::Location loc);

private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
};
class _JitFusedMatMulOp : public ::mlir::Op<_JitFusedMatMulOp, ::mlir::OpTrait::ZeroRegion, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::TensorType>::Impl, ::mlir::OpTrait::ZeroSuccessor, ::mlir::OpTrait::AtLeastNOperands<2>::Impl, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::OpTrait::SameOperandsAndResultElementType, ::mlir::DerivedAttributeOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _JitFusedMatMulOpAdaptor;
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("transpose_a"), ::llvm::StringRef("transpose_b"), ::llvm::StringRef("fusion"), ::llvm::StringRef("T")};
  return ::llvm::makeArrayRef(attrNames);
  }
  ::mlir::Identifier transpose_aAttrName() {
    return getAttributeNameForIndex(0);
  }
  static ::mlir::Identifier transpose_aAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }
  ::mlir::Identifier transpose_bAttrName() {
    return getAttributeNameForIndex(1);
  }
  static ::mlir::Identifier transpose_bAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }
  ::mlir::Identifier fusionAttrName() {
    return getAttributeNameForIndex(2);
  }
  static ::mlir::Identifier fusionAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }
  ::mlir::Identifier TAttrName() {
    return getAttributeNameForIndex(3);
  }
  static ::mlir::Identifier TAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }
  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._JitFusedMatMul");
  }
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value a();
  ::mlir::Value b();
  ::mlir::Operation::operand_range additional_args();
  ::mlir::MutableOperandRange aMutable();
  ::mlir::MutableOperandRange bMutable();
  ::mlir::MutableOperandRange additional_argsMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Value product();
  ::mlir::BoolAttr transpose_aAttr();
  bool transpose_a();
  ::mlir::BoolAttr transpose_bAttr();
  bool transpose_b();
  ::mlir::ArrayAttr fusionAttr();
  ::mlir::ArrayAttr fusion();
  Type T();
  static bool isDerivedAttribute(::llvm::StringRef name);
  ::mlir::DictionaryAttr materializeDerivedAttributes();
  void transpose_aAttr(::mlir::BoolAttr attr);
  void transpose_bAttr(::mlir::BoolAttr attr);
  void fusionAttr(::mlir::ArrayAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type product, ::mlir::Value a, ::mlir::Value b, ::mlir::ValueRange additional_args, ::mlir::BoolAttr transpose_a, ::mlir::BoolAttr transpose_b, ::mlir::ArrayAttr fusion);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value a, ::mlir::Value b, ::mlir::ValueRange additional_args, ::mlir::BoolAttr transpose_a, ::mlir::BoolAttr transpose_b, ::mlir::ArrayAttr fusion);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type product, ::mlir::Value a, ::mlir::Value b, ::mlir::ValueRange additional_args, bool transpose_a, bool transpose_b, ::mlir::ArrayAttr fusion);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value a, ::mlir::Value b, ::mlir::ValueRange additional_args, bool transpose_a, bool transpose_b, ::mlir::ArrayAttr fusion);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verify();
  void getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);

private:
  ::mlir::Identifier getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }
  static ::mlir::Identifier getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
  assert(index < 4 && "invalid attribute index");
  return name.getAbstractOperation()->getAttributeNames()[index];
  }
};
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_TfrtGetResourceOp declarations
//===----------------------------------------------------------------------===//

class _TfrtGetResourceOpAdaptor {
public:
  _TfrtGetResourceOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});
  _TfrtGetResourceOpAdaptor(_TfrtGetResourceOp&op);
  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::ArrayAttr indices();
  ::mlir::LogicalResult verify(::mlir::Location loc);

private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
};
class _TfrtGetResourceOp : public ::mlir::Op<_TfrtGetResourceOp, ::mlir::OpTrait::ZeroRegion, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessor, ::mlir::OpTrait::ZeroOperands, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::OpTrait::TF::NoConstantFold> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _TfrtGetResourceOpAdaptor;
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("indices")};
  return ::llvm::makeArrayRef(attrNames);
  }
  ::mlir::Identifier indicesAttrName() {
    return getAttributeNameForIndex(0);
  }
  static ::mlir::Identifier indicesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }
  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._TfrtGetResource");
  }
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range results();
  ::mlir::ArrayAttr indicesAttr();
  ::mlir::ArrayAttr indices();
  void indicesAttr(::mlir::ArrayAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange results, ::mlir::ArrayAttr indices);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verify();
  void getEffects(::mlir::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);

private:
  ::mlir::Identifier getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }
  static ::mlir::Identifier getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
  assert(index < 1 && "invalid attribute index");
  return name.getAbstractOperation()->getAttributeNames()[index];
  }
};
} // namespace TF
} // namespace mlir
namespace mlir {
namespace TF {

//===----------------------------------------------------------------------===//
// ::mlir::TF::_TfrtSetResourceOp declarations
//===----------------------------------------------------------------------===//

class _TfrtSetResourceOpAdaptor {
public:
  _TfrtSetResourceOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});
  _TfrtSetResourceOpAdaptor(_TfrtSetResourceOp&op);
  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value arg();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::IntegerAttr index();
  ::mlir::LogicalResult verify(::mlir::Location loc);

private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
};
class _TfrtSetResourceOp : public ::mlir::Op<_TfrtSetResourceOp, ::mlir::OpTrait::ZeroRegion, ::mlir::OpTrait::ZeroResult, ::mlir::OpTrait::ZeroSuccessor, ::mlir::OpTrait::OneOperand> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = _TfrtSetResourceOpAdaptor;
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("index")};
  return ::llvm::makeArrayRef(attrNames);
  }
  ::mlir::Identifier indexAttrName() {
    return getAttributeNameForIndex(0);
  }
  static ::mlir::Identifier indexAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }
  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("tf._TfrtSetResource");
  }
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value arg();
  ::mlir::MutableOperandRange argMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::IntegerAttr indexAttr();
  uint64_t index();
  void indexAttr(::mlir::IntegerAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value arg, ::mlir::IntegerAttr index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value arg, ::mlir::IntegerAttr index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value arg, uint64_t index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value arg, uint64_t index);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verify();

private:
  ::mlir::Identifier getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }
  static ::mlir::Identifier getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
  assert(index < 1 && "invalid attribute index");
  return name.getAbstractOperation()->getAttributeNames()[index];
  }
};
} // namespace TF
} // namespace mlir

#endif  // GET_OP_CLASSES

