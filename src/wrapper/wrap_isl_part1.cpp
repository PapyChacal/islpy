#include "wrap_isl.hpp"

namespace isl
{
#include "gen-wrap-part1.inc"

  class constants { };
}

namespace islpy
{
  bool id_eq(isl::id const *self, isl::id const *other)
  {
    return self == other;
  }

  bool id_ne(isl::id const *self, isl::id const *other)
  {
    return self != other;
  }
}

void islpy_expose_part1(py::module &m)
{
  {
    typedef isl::ctx cls;
    py::class_<cls, std::shared_ptr<cls> >
      wrap_ctx(m, "Context");
    wrap_ctx.def(py::init(
          []()
          {
            isl_ctx *result = isl_ctx_alloc();
            if (result)
            {
              try
              { return new isl::ctx(result); }
              catch (...)
              {
                isl_ctx_free(result);
                throw;
              }
            }
            else
              PYTHON_ERROR(RuntimeError, "failed to create context");
          }));
    wrap_ctx.attr("_base_name") = "ctx";
    wrap_ctx.attr("_isl_name") = "isl_ctx";
  }

#define CONST(NAME) cls.attr(#NAME) = ISL_##NAME
  {
    py::class_<isl::constants> cls(m, "constants");
    CONST(BOUND_BERNSTEIN);
    CONST(BOUND_RANGE);
    CONST(ON_ERROR_WARN);
    CONST(ON_ERROR_CONTINUE);
    CONST(ON_ERROR_ABORT);
    CONST(SCHEDULE_ALGORITHM_ISL);
    CONST(SCHEDULE_ALGORITHM_FEAUTRIER);
  }

  // {{{ lists

  MAKE_WRAP(id_list, IdList);
  MAKE_WRAP(val_list, ValList);
  MAKE_WRAP(basic_set_list, BasicSetList);
  MAKE_WRAP(basic_map_list, BasicMapList);
  MAKE_WRAP(set_list, SetList);
  MAKE_WRAP(map_list, MapList);
  MAKE_WRAP(union_set_list, UnionSetList);
  MAKE_WRAP(constraint_list, ConstraintList);
  MAKE_WRAP(aff_list, AffList);
  MAKE_WRAP(pw_aff_list, PwAffList);
  MAKE_WRAP(pw_multi_aff_list, PwMultiAffList);
  MAKE_WRAP(ast_expr_list, AstExprList);
  MAKE_WRAP(ast_node_list, AstNodeList);
  MAKE_WRAP(pw_qpolynomial_list, PwQPolynomialList);
  MAKE_WRAP(pw_qpolynomial_fold_list, PwQPolynomialFoldList);
  MAKE_WRAP(union_pw_aff_list, UnionPwAffList);
  MAKE_WRAP(union_pw_multi_aff_list, UnionPwMultiAffList);
  MAKE_WRAP(union_map_list, UnionMapList);

  // }}}

  // {{{ maps

  MAKE_WRAP(id_to_ast_expr, IdToAstExpr);

  // }}}

  MAKE_WRAP(printer, Printer);
  MAKE_WRAP(val, Val);

  MAKE_WRAP(multi_val, MultiVal);
  MAKE_WRAP(vec, Vec);
  MAKE_WRAP(mat, Mat);
  MAKE_WRAP(fixed_box, FixedBox);

  MAKE_WRAP(aff, Aff);
  // wrap_aff.enable_pickling();
  MAKE_WRAP(pw_aff, PwAff);
  // wrap_pw_aff.enable_pickling();
  MAKE_WRAP(union_pw_aff, UnionPwAff);
  // wrap_union_pw_aff.enable_pickling();
  MAKE_WRAP(multi_id, MultiId);
  MAKE_WRAP(multi_aff, MultiAff);
  // wrap_multi_aff.enable_pickling();
  MAKE_WRAP(multi_pw_aff, MultiPwAff);
  // wrap_multi_pw_aff.enable_pickling();
  MAKE_WRAP(pw_multi_aff, PwMultiAff);
  // wrap_pw_multi_aff.enable_pickling();
  MAKE_WRAP(union_pw_multi_aff, UnionPwMultiAff);
  // wrap_union_pw_multi_aff.enable_pickling();
  MAKE_WRAP(multi_union_pw_aff, MultiUnionPwAff);
  // wrap_multi_union_pw_aff.enable_pickling();

  MAKE_WRAP(id, Id);
  wrap_id.def("__eq__", islpy::id_eq, py::arg("other"),
      "__eq__(self, other)\n\n"
      ":param self: :class:`Id`\n"
      ":param other: :class:`Id`\n"
      ":return: bool ");
  wrap_id.def("__ne__", islpy::id_ne, py::arg("other"),
      "__ne__(self, other)\n\n"
      ":param self: :class:`Id`\n"
      ":param other: :class:`Id`\n"
      ":return: bool ");

  MAKE_WRAP(constraint, Constraint);
  // wrap_constraint.enable_pickling();
  MAKE_WRAP(space, Space);
  MAKE_WRAP(local_space, LocalSpace);

#include "gen-expose-part1.inc"
}
