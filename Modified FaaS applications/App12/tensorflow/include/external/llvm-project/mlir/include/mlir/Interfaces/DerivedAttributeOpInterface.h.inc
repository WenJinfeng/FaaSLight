/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
class DerivedAttributeOpInterface;
namespace detail {
struct DerivedAttributeOpInterfaceInterfaceTraits {
  struct Concept {
    bool (*isDerivedAttribute)(StringRef);
    DictionaryAttr (*materializeDerivedAttributes)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::DerivedAttributeOpInterface;
    Model() : Concept{isDerivedAttribute, materializeDerivedAttributes} {}

    static inline bool isDerivedAttribute(StringRef name);
    static inline DictionaryAttr materializeDerivedAttributes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::DerivedAttributeOpInterface;
    FallbackModel() : Concept{isDerivedAttribute, materializeDerivedAttributes} {}

    static inline bool isDerivedAttribute(StringRef name);
    static inline DictionaryAttr materializeDerivedAttributes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
  };
};template <typename ConcreteOp>
struct DerivedAttributeOpInterfaceTrait;

} // end namespace detail
class DerivedAttributeOpInterface : public ::mlir::OpInterface<DerivedAttributeOpInterface, detail::DerivedAttributeOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<DerivedAttributeOpInterface, detail::DerivedAttributeOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::DerivedAttributeOpInterfaceTrait<ConcreteOp> {};
  bool isDerivedAttribute(StringRef name);
  DictionaryAttr materializeDerivedAttributes();
};
namespace detail {
  template <typename ConcreteOp>
  struct DerivedAttributeOpInterfaceTrait : public ::mlir::OpInterface<DerivedAttributeOpInterface, detail::DerivedAttributeOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
template<typename ConcreteOp>
bool detail::DerivedAttributeOpInterfaceInterfaceTraits::Model<ConcreteOp>::isDerivedAttribute(StringRef name) {
  return ConcreteOp::isDerivedAttribute(name);
}
template<typename ConcreteOp>
DictionaryAttr detail::DerivedAttributeOpInterfaceInterfaceTraits::Model<ConcreteOp>::materializeDerivedAttributes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).materializeDerivedAttributes();
}
template<typename ConcreteOp>
bool detail::DerivedAttributeOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::isDerivedAttribute(StringRef name) {
  return ConcreteOp::isDerivedAttribute(name);
}
template<typename ConcreteOp>
DictionaryAttr detail::DerivedAttributeOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::materializeDerivedAttributes(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->materializeDerivedAttributes(tablegen_opaque_val);
}
} // namespace mlir
