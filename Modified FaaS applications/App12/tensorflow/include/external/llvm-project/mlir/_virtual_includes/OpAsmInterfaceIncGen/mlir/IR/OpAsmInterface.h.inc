/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
class OpAsmOpInterface;
namespace detail {
struct OpAsmOpInterfaceInterfaceTraits {
  struct Concept {
    void (*getAsmResultNames)(const Concept *impl, ::mlir::Operation *, ::mlir::OpAsmSetValueNameFn);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::OpAsmOpInterface;
    Model() : Concept{getAsmResultNames} {}

    static inline void getAsmResultNames(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::OpAsmSetValueNameFn setNameFn);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::OpAsmOpInterface;
    FallbackModel() : Concept{getAsmResultNames} {}

    static inline void getAsmResultNames(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::OpAsmSetValueNameFn setNameFn);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
  };
};template <typename ConcreteOp>
struct OpAsmOpInterfaceTrait;

} // end namespace detail
class OpAsmOpInterface : public ::mlir::OpInterface<OpAsmOpInterface, detail::OpAsmOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<OpAsmOpInterface, detail::OpAsmOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::OpAsmOpInterfaceTrait<ConcreteOp> {};
  void getAsmResultNames(::mlir::OpAsmSetValueNameFn setNameFn);
};
namespace detail {
  template <typename ConcreteOp>
  struct OpAsmOpInterfaceTrait : public ::mlir::OpInterface<OpAsmOpInterface, detail::OpAsmOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
template<typename ConcreteOp>
void detail::OpAsmOpInterfaceInterfaceTraits::Model<ConcreteOp>::getAsmResultNames(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::OpAsmSetValueNameFn setNameFn) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getAsmResultNames(setNameFn);
}
template<typename ConcreteOp>
void detail::OpAsmOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getAsmResultNames(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::OpAsmSetValueNameFn setNameFn) {
  return static_cast<const ConcreteOp *>(impl)->getAsmResultNames(tablegen_opaque_val, setNameFn);
}
} // namespace mlir
