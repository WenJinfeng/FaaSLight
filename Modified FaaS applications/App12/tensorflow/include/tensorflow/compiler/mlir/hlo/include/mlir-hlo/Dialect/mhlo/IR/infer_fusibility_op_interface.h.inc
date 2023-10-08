/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

class InferFusibilityOpInterface;
namespace detail {
struct InferFusibilityOpInterfaceInterfaceTraits {
  struct Concept {
    bool (*isFusibleWithOperand)(const Concept *impl, ::mlir::Operation *);
    bool (*isFusibleWithConsumer)(const Concept *impl, ::mlir::Operation *);
    bool (*inferInputsShapeEquality)(const Concept *impl, ::mlir::Operation *, int, int);
    bool (*inferOutputsShapeEquality)(const Concept *impl, ::mlir::Operation *, int, int);
    bool (*inferInputOutputShapeEquality)(const Concept *impl, ::mlir::Operation *, int, int);
    llvm::Optional<Value> (*inferEffectiveWorkloadShape)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = InferFusibilityOpInterface;
    Model() : Concept{isFusibleWithOperand, isFusibleWithConsumer, inferInputsShapeEquality, inferOutputsShapeEquality, inferInputOutputShapeEquality, inferEffectiveWorkloadShape} {}

    static inline bool isFusibleWithOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool isFusibleWithConsumer(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool inferInputsShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int lhs, int rhs);
    static inline bool inferOutputsShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int lhs, int rhs);
    static inline bool inferInputOutputShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int input, int output);
    static inline llvm::Optional<Value> inferEffectiveWorkloadShape(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = InferFusibilityOpInterface;
    FallbackModel() : Concept{isFusibleWithOperand, isFusibleWithConsumer, inferInputsShapeEquality, inferOutputsShapeEquality, inferInputOutputShapeEquality, inferEffectiveWorkloadShape} {}

    static inline bool isFusibleWithOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool isFusibleWithConsumer(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline bool inferInputsShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int lhs, int rhs);
    static inline bool inferOutputsShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int lhs, int rhs);
    static inline bool inferInputOutputShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int input, int output);
    static inline llvm::Optional<Value> inferEffectiveWorkloadShape(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    bool isFusibleWithOperand(::mlir::Operation *tablegen_opaque_val) const;
    bool isFusibleWithConsumer(::mlir::Operation *tablegen_opaque_val) const;
    bool inferInputsShapeEquality(::mlir::Operation *tablegen_opaque_val, int lhs, int rhs) const;
    bool inferOutputsShapeEquality(::mlir::Operation *tablegen_opaque_val, int lhs, int rhs) const;
    bool inferInputOutputShapeEquality(::mlir::Operation *tablegen_opaque_val, int input, int output) const;
    llvm::Optional<Value> inferEffectiveWorkloadShape(::mlir::Operation *tablegen_opaque_val) const;
  };
};template <typename ConcreteOp>
struct InferFusibilityOpInterfaceTrait;

} // end namespace detail
class InferFusibilityOpInterface : public ::mlir::OpInterface<InferFusibilityOpInterface, detail::InferFusibilityOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<InferFusibilityOpInterface, detail::InferFusibilityOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::InferFusibilityOpInterfaceTrait<ConcreteOp> {};
  bool isFusibleWithOperand();
  bool isFusibleWithConsumer();
  bool inferInputsShapeEquality(int lhs, int rhs);
  bool inferOutputsShapeEquality(int lhs, int rhs);
  bool inferInputOutputShapeEquality(int input, int output);
  llvm::Optional<Value> inferEffectiveWorkloadShape();

    // Returns whether the given values have the same static shape.
    static bool inferShapeEquality(Value first, Value second) {
      // If both lhs and rhs have static shapes, check them directly.
      auto first_ty = first.getType().dyn_cast<RankedTensorType>();
      auto second_ty = second.getType().dyn_cast<RankedTensorType>();
      if (!first_ty || !first_ty.hasStaticShape() ||
          !second_ty || !second_ty.hasStaticShape() ||
          first_ty.getRank() != second_ty.getRank()) {
        return false;
      }
      return first_ty.getShape() == second_ty.getShape();
    }
  
};
namespace detail {
  template <typename ConcreteOp>
  struct InferFusibilityOpInterfaceTrait : public ::mlir::OpInterface<InferFusibilityOpInterface, detail::InferFusibilityOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
    bool isFusibleWithOperand() {
      /// Returns whether this op can be fused with its operands
        return true;
    }
    bool isFusibleWithConsumer() {
      /// Return whether this op can be fused with its consumers
        return true;
    }
    bool inferInputsShapeEquality(int lhs, int rhs) {
      /// Return whether two inputs have the same shape.
        Operation *op = this->getOperation();
        assert(lhs >= 0 && rhs >= 0);
        if (lhs == rhs) return true;
        return InferFusibilityOpInterface::inferShapeEquality(op->getOperand(lhs), op->getOperand(rhs));
    }
    bool inferOutputsShapeEquality(int lhs, int rhs) {
      /// Return whether two outputs have the same shape.
        Operation *op = this->getOperation();
        assert(lhs >= 0 && rhs >= 0);
        if (lhs == rhs) return true;
        return InferFusibilityOpInterface::inferShapeEquality(op->getResult(lhs), op->getResult(rhs));
    }
    bool inferInputOutputShapeEquality(int input, int output) {
      /// Return whether the input and the output have the same shape.
        Operation *op = this->getOperation();
        assert(input >= 0 && output >= 0);
        return InferFusibilityOpInterface::inferShapeEquality(op->getOperand(input), op->getResult(output));
    }
    llvm::Optional<Value> inferEffectiveWorkloadShape() {
      /// Return effective workload size if possible, otherwise None.
        return {};
    }
  };
}// namespace detail
template<typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::Model<ConcreteOp>::isFusibleWithOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).isFusibleWithOperand();
}
template<typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::Model<ConcreteOp>::isFusibleWithConsumer(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).isFusibleWithConsumer();
}
template<typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::Model<ConcreteOp>::inferInputsShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int lhs, int rhs) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).inferInputsShapeEquality(lhs, rhs);
}
template<typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::Model<ConcreteOp>::inferOutputsShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int lhs, int rhs) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).inferOutputsShapeEquality(lhs, rhs);
}
template<typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::Model<ConcreteOp>::inferInputOutputShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int input, int output) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).inferInputOutputShapeEquality(input, output);
}
template<typename ConcreteOp>
llvm::Optional<Value> detail::InferFusibilityOpInterfaceInterfaceTraits::Model<ConcreteOp>::inferEffectiveWorkloadShape(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).inferEffectiveWorkloadShape();
}
template<typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::isFusibleWithOperand(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->isFusibleWithOperand(tablegen_opaque_val);
}
template<typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::isFusibleWithConsumer(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->isFusibleWithConsumer(tablegen_opaque_val);
}
template<typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::inferInputsShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int lhs, int rhs) {
  return static_cast<const ConcreteOp *>(impl)->inferInputsShapeEquality(tablegen_opaque_val, lhs, rhs);
}
template<typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::inferOutputsShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int lhs, int rhs) {
  return static_cast<const ConcreteOp *>(impl)->inferOutputsShapeEquality(tablegen_opaque_val, lhs, rhs);
}
template<typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::inferInputOutputShapeEquality(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, int input, int output) {
  return static_cast<const ConcreteOp *>(impl)->inferInputOutputShapeEquality(tablegen_opaque_val, input, output);
}
template<typename ConcreteOp>
llvm::Optional<Value> detail::InferFusibilityOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::inferEffectiveWorkloadShape(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->inferEffectiveWorkloadShape(tablegen_opaque_val);
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::isFusibleWithOperand(::mlir::Operation *tablegen_opaque_val) const {
/// Returns whether this op can be fused with its operands
        return true;
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::isFusibleWithConsumer(::mlir::Operation *tablegen_opaque_val) const {
/// Return whether this op can be fused with its consumers
        return true;
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::inferInputsShapeEquality(::mlir::Operation *tablegen_opaque_val, int lhs, int rhs) const {
/// Return whether two inputs have the same shape.
        Operation *op = this->getOperation();
        assert(lhs >= 0 && rhs >= 0);
        if (lhs == rhs) return true;
        return InferFusibilityOpInterface::inferShapeEquality(op->getOperand(lhs), op->getOperand(rhs));
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::inferOutputsShapeEquality(::mlir::Operation *tablegen_opaque_val, int lhs, int rhs) const {
/// Return whether two outputs have the same shape.
        Operation *op = this->getOperation();
        assert(lhs >= 0 && rhs >= 0);
        if (lhs == rhs) return true;
        return InferFusibilityOpInterface::inferShapeEquality(op->getResult(lhs), op->getResult(rhs));
}
template<typename ConcreteModel, typename ConcreteOp>
bool detail::InferFusibilityOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::inferInputOutputShapeEquality(::mlir::Operation *tablegen_opaque_val, int input, int output) const {
/// Return whether the input and the output have the same shape.
        Operation *op = this->getOperation();
        assert(input >= 0 && output >= 0);
        return InferFusibilityOpInterface::inferShapeEquality(op->getOperand(input), op->getResult(output));
}
template<typename ConcreteModel, typename ConcreteOp>
llvm::Optional<Value> detail::InferFusibilityOpInterfaceInterfaceTraits::ExternalModel<ConcreteModel, ConcreteOp>::inferEffectiveWorkloadShape(::mlir::Operation *tablegen_opaque_val) const {
/// Return effective workload size if possible, otherwise None.
        return {};
}
