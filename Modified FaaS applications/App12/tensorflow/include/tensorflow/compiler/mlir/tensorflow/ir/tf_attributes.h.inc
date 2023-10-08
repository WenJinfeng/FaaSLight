/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES


namespace mlir {
class DialectAsmParser;
class DialectAsmPrinter;
} // namespace mlir
namespace mlir {
namespace TF {
  class FuncAttr;
  class PlaceholderAttr;
  class ShapeAttr;

  namespace detail {
    struct FuncAttrStorage;
  } // end namespace detail
  class FuncAttr : public ::mlir::Attribute::AttrBase<FuncAttr, ::mlir::Attribute,
                                         detail::FuncAttrStorage> {
  public:
    /// Inherit some necessary constructors from 'AttrBase'.
    using Base::Base;

    static FuncAttr get(::mlir::MLIRContext *context, SymbolRefAttr name, DictionaryAttr attrs);
    static FuncAttr get(::mlir::MLIRContext *context, StringRef name, DictionaryAttr attr);
    static constexpr ::llvm::StringLiteral getMnemonic() {
      return ::llvm::StringLiteral("func");
    }

    static ::mlir::Attribute parse(::mlir::MLIRContext *context,
                             ::mlir::DialectAsmParser &parser, ::mlir::Type type);
    void print(::mlir::DialectAsmPrinter &printer) const;
    SymbolRefAttr getName() const;
    DictionaryAttr getAttrs() const;
  };

  namespace detail {
    struct PlaceholderAttrStorage;
  } // end namespace detail
  class PlaceholderAttr : public ::mlir::Attribute::AttrBase<PlaceholderAttr, ::mlir::Attribute,
                                         detail::PlaceholderAttrStorage> {
  public:
    /// Inherit some necessary constructors from 'AttrBase'.
    using Base::Base;

    static PlaceholderAttr get(::mlir::MLIRContext *context, ::llvm::StringRef value);
    static constexpr ::llvm::StringLiteral getMnemonic() {
      return ::llvm::StringLiteral("placeholder");
    }

    static ::mlir::Attribute parse(::mlir::MLIRContext *context,
                             ::mlir::DialectAsmParser &parser, ::mlir::Type type);
    void print(::mlir::DialectAsmPrinter &printer) const;
    ::llvm::StringRef getValue() const;
  };

  namespace detail {
    struct ShapeAttrStorage;
  } // end namespace detail
  class ShapeAttr : public ::mlir::Attribute::AttrBase<ShapeAttr, ::mlir::Attribute,
                                         detail::ShapeAttrStorage> {
  public:
    /// Inherit some necessary constructors from 'AttrBase'.
    using Base::Base;


    // Returns true if this shape is ranked and no dimension has unknown size
    // (ShapedType::kDynamicDim).
    bool hasStaticShape() const;

    bool hasRank() const;

    // If this is ranked, return the rank. Otherwise, abort.
    int64_t getRank() const;

    // Return the shape array if ranked.
    llvm::Optional<ArrayRef<int64_t>> getValue() const;
  
    static ShapeAttr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<int64_t> shape, bool unranked);
    static ShapeAttr get(::mlir::MLIRContext *context, llvm::Optional<ArrayRef<int64_t>> dimensions);
    static ShapeAttr get(::mlir::MLIRContext *context, ShapedType shaped_type);
    static constexpr ::llvm::StringLiteral getMnemonic() {
      return ::llvm::StringLiteral("shape");
    }

    static ::mlir::Attribute parse(::mlir::MLIRContext *context,
                             ::mlir::DialectAsmParser &parser, ::mlir::Type type);
    void print(::mlir::DialectAsmPrinter &printer) const;
    ::llvm::ArrayRef<int64_t> getShape() const;
    bool getUnranked() const;
  };
} // namespace TF
} // namespace mlir

#endif  // GET_ATTRDEF_CLASSES

