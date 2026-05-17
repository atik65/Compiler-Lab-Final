/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison implementation for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output, and Bison version.  */
#define YYBISON 30802

/* Bison version string.  */
#define YYBISON_VERSION "3.8.2"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1




/* First part of user prologue.  */
#line 1 "parser.y"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex();
void yyerror(const char *s);
extern FILE *yyin;
int line_no = 1;

char current_type[20] = "";
int mem_address = 1000;

typedef struct SymbolEntry {
    char token[100];
    char data_type[20];
    char token_type[20];
    char token_value[100];
    int line;
    char dimension[20];
    char address[20];
    struct SymbolEntry *next;
} SymbolEntry;

SymbolEntry *symbol_table = NULL;

void insert_symbol(char *token, char *data_type, char *token_type, char *token_value, int line, char *dimension, char *address);
void print_symbol_table();
SymbolEntry* lookup_symbol(char *token);

#line 102 "parser.tab.c"

# ifndef YY_CAST
#  ifdef __cplusplus
#   define YY_CAST(Type, Val) static_cast<Type> (Val)
#   define YY_REINTERPRET_CAST(Type, Val) reinterpret_cast<Type> (Val)
#  else
#   define YY_CAST(Type, Val) ((Type) (Val))
#   define YY_REINTERPRET_CAST(Type, Val) ((Type) (Val))
#  endif
# endif
# ifndef YY_NULLPTR
#  if defined __cplusplus
#   if 201103L <= __cplusplus
#    define YY_NULLPTR nullptr
#   else
#    define YY_NULLPTR 0
#   endif
#  else
#   define YY_NULLPTR ((void*)0)
#  endif
# endif

#include "parser.tab.h"
/* Symbol kind.  */
enum yysymbol_kind_t
{
  YYSYMBOL_YYEMPTY = -2,
  YYSYMBOL_YYEOF = 0,                      /* "end of file"  */
  YYSYMBOL_YYerror = 1,                    /* error  */
  YYSYMBOL_YYUNDEF = 2,                    /* "invalid token"  */
  YYSYMBOL_IDENTIFIER = 3,                 /* IDENTIFIER  */
  YYSYMBOL_INT_CONST = 4,                  /* INT_CONST  */
  YYSYMBOL_FLOAT_CONST = 5,                /* FLOAT_CONST  */
  YYSYMBOL_STRING_CONST = 6,               /* STRING_CONST  */
  YYSYMBOL_CHAR_CONST = 7,                 /* CHAR_CONST  */
  YYSYMBOL_INT = 8,                        /* INT  */
  YYSYMBOL_FLOAT_TYPE = 9,                 /* FLOAT_TYPE  */
  YYSYMBOL_CHAR_TYPE = 10,                 /* CHAR_TYPE  */
  YYSYMBOL_DOUBLE = 11,                    /* DOUBLE  */
  YYSYMBOL_VOID = 12,                      /* VOID  */
  YYSYMBOL_IF = 13,                        /* IF  */
  YYSYMBOL_ELSE = 14,                      /* ELSE  */
  YYSYMBOL_WHILE = 15,                     /* WHILE  */
  YYSYMBOL_FOR = 16,                       /* FOR  */
  YYSYMBOL_RETURN = 17,                    /* RETURN  */
  YYSYMBOL_PRINTF = 18,                    /* PRINTF  */
  YYSYMBOL_SCANF = 19,                     /* SCANF  */
  YYSYMBOL_PLUS = 20,                      /* PLUS  */
  YYSYMBOL_MINUS = 21,                     /* MINUS  */
  YYSYMBOL_MULT = 22,                      /* MULT  */
  YYSYMBOL_DIV = 23,                       /* DIV  */
  YYSYMBOL_ASSIGN = 24,                    /* ASSIGN  */
  YYSYMBOL_EQ = 25,                        /* EQ  */
  YYSYMBOL_NE = 26,                        /* NE  */
  YYSYMBOL_LT = 27,                        /* LT  */
  YYSYMBOL_GT = 28,                        /* GT  */
  YYSYMBOL_LE = 29,                        /* LE  */
  YYSYMBOL_GE = 30,                        /* GE  */
  YYSYMBOL_AND = 31,                       /* AND  */
  YYSYMBOL_OR = 32,                        /* OR  */
  YYSYMBOL_NOT = 33,                       /* NOT  */
  YYSYMBOL_LPAREN = 34,                    /* LPAREN  */
  YYSYMBOL_RPAREN = 35,                    /* RPAREN  */
  YYSYMBOL_LBRACE = 36,                    /* LBRACE  */
  YYSYMBOL_RBRACE = 37,                    /* RBRACE  */
  YYSYMBOL_LBRACKET = 38,                  /* LBRACKET  */
  YYSYMBOL_RBRACKET = 39,                  /* RBRACKET  */
  YYSYMBOL_SEMICOLON = 40,                 /* SEMICOLON  */
  YYSYMBOL_COMMA = 41,                     /* COMMA  */
  YYSYMBOL_YYACCEPT = 42,                  /* $accept  */
  YYSYMBOL_program = 43,                   /* program  */
  YYSYMBOL_external_declaration = 44,      /* external_declaration  */
  YYSYMBOL_function_definition = 45,       /* function_definition  */
  YYSYMBOL_parameter_list = 46,            /* parameter_list  */
  YYSYMBOL_compound_statement = 47,        /* compound_statement  */
  YYSYMBOL_statement_list = 48,            /* statement_list  */
  YYSYMBOL_statement = 49,                 /* statement  */
  YYSYMBOL_declaration = 50,               /* declaration  */
  YYSYMBOL_type = 51,                      /* type  */
  YYSYMBOL_assignment = 52,                /* assignment  */
  YYSYMBOL_expression = 53,                /* expression  */
  YYSYMBOL_term = 54,                      /* term  */
  YYSYMBOL_factor = 55,                    /* factor  */
  YYSYMBOL_if_statement = 56,              /* if_statement  */
  YYSYMBOL_loop_statement = 57,            /* loop_statement  */
  YYSYMBOL_condition = 58,                 /* condition  */
  YYSYMBOL_relational_op = 59,             /* relational_op  */
  YYSYMBOL_function_call = 60,             /* function_call  */
  YYSYMBOL_argument_list = 61,             /* argument_list  */
  YYSYMBOL_return_statement = 62           /* return_statement  */
};
typedef enum yysymbol_kind_t yysymbol_kind_t;




#ifdef short
# undef short
#endif

/* On compilers that do not define __PTRDIFF_MAX__ etc., make sure
   <limits.h> and (if available) <stdint.h> are included
   so that the code can choose integer types of a good width.  */

#ifndef __PTRDIFF_MAX__
# include <limits.h> /* INFRINGES ON USER NAME SPACE */
# if defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stdint.h> /* INFRINGES ON USER NAME SPACE */
#  define YY_STDINT_H
# endif
#endif

/* Narrow types that promote to a signed type and that can represent a
   signed or unsigned integer of at least N bits.  In tables they can
   save space and decrease cache pressure.  Promoting to a signed type
   helps avoid bugs in integer arithmetic.  */

#ifdef __INT_LEAST8_MAX__
typedef __INT_LEAST8_TYPE__ yytype_int8;
#elif defined YY_STDINT_H
typedef int_least8_t yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef __INT_LEAST16_MAX__
typedef __INT_LEAST16_TYPE__ yytype_int16;
#elif defined YY_STDINT_H
typedef int_least16_t yytype_int16;
#else
typedef short yytype_int16;
#endif

/* Work around bug in HP-UX 11.23, which defines these macros
   incorrectly for preprocessor constants.  This workaround can likely
   be removed in 2023, as HPE has promised support for HP-UX 11.23
   (aka HP-UX 11i v2) only through the end of 2022; see Table 2 of
   <https://h20195.www2.hpe.com/V2/getpdf.aspx/4AA4-7673ENW.pdf>.  */
#ifdef __hpux
# undef UINT_LEAST8_MAX
# undef UINT_LEAST16_MAX
# define UINT_LEAST8_MAX 255
# define UINT_LEAST16_MAX 65535
#endif

#if defined __UINT_LEAST8_MAX__ && __UINT_LEAST8_MAX__ <= __INT_MAX__
typedef __UINT_LEAST8_TYPE__ yytype_uint8;
#elif (!defined __UINT_LEAST8_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST8_MAX <= INT_MAX)
typedef uint_least8_t yytype_uint8;
#elif !defined __UINT_LEAST8_MAX__ && UCHAR_MAX <= INT_MAX
typedef unsigned char yytype_uint8;
#else
typedef short yytype_uint8;
#endif

#if defined __UINT_LEAST16_MAX__ && __UINT_LEAST16_MAX__ <= __INT_MAX__
typedef __UINT_LEAST16_TYPE__ yytype_uint16;
#elif (!defined __UINT_LEAST16_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST16_MAX <= INT_MAX)
typedef uint_least16_t yytype_uint16;
#elif !defined __UINT_LEAST16_MAX__ && USHRT_MAX <= INT_MAX
typedef unsigned short yytype_uint16;
#else
typedef int yytype_uint16;
#endif

#ifndef YYPTRDIFF_T
# if defined __PTRDIFF_TYPE__ && defined __PTRDIFF_MAX__
#  define YYPTRDIFF_T __PTRDIFF_TYPE__
#  define YYPTRDIFF_MAXIMUM __PTRDIFF_MAX__
# elif defined PTRDIFF_MAX
#  ifndef ptrdiff_t
#   include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  endif
#  define YYPTRDIFF_T ptrdiff_t
#  define YYPTRDIFF_MAXIMUM PTRDIFF_MAX
# else
#  define YYPTRDIFF_T long
#  define YYPTRDIFF_MAXIMUM LONG_MAX
# endif
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned
# endif
#endif

#define YYSIZE_MAXIMUM                                  \
  YY_CAST (YYPTRDIFF_T,                                 \
           (YYPTRDIFF_MAXIMUM < YY_CAST (YYSIZE_T, -1)  \
            ? YYPTRDIFF_MAXIMUM                         \
            : YY_CAST (YYSIZE_T, -1)))

#define YYSIZEOF(X) YY_CAST (YYPTRDIFF_T, sizeof (X))


/* Stored state numbers (used for stacks). */
typedef yytype_uint8 yy_state_t;

/* State numbers in computations.  */
typedef int yy_state_fast_t;

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif


#ifndef YY_ATTRIBUTE_PURE
# if defined __GNUC__ && 2 < __GNUC__ + (96 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_PURE __attribute__ ((__pure__))
# else
#  define YY_ATTRIBUTE_PURE
# endif
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# if defined __GNUC__ && 2 < __GNUC__ + (7 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_UNUSED __attribute__ ((__unused__))
# else
#  define YY_ATTRIBUTE_UNUSED
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YY_USE(E) ((void) (E))
#else
# define YY_USE(E) /* empty */
#endif

/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
#if defined __GNUC__ && ! defined __ICC && 406 <= __GNUC__ * 100 + __GNUC_MINOR__
# if __GNUC__ * 100 + __GNUC_MINOR__ < 407
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")
# else
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")              \
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# endif
# define YY_IGNORE_MAYBE_UNINITIALIZED_END      \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif

#if defined __cplusplus && defined __GNUC__ && ! defined __ICC && 6 <= __GNUC__
# define YY_IGNORE_USELESS_CAST_BEGIN                          \
    _Pragma ("GCC diagnostic push")                            \
    _Pragma ("GCC diagnostic ignored \"-Wuseless-cast\"")
# define YY_IGNORE_USELESS_CAST_END            \
    _Pragma ("GCC diagnostic pop")
#endif
#ifndef YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_END
#endif


#define YY_ASSERT(E) ((void) (0 && (E)))

#if !defined yyoverflow

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* !defined yyoverflow */

#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yy_state_t yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (YYSIZEOF (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (YYSIZEOF (yy_state_t) + YYSIZEOF (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYPTRDIFF_T yynewbytes;                                         \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * YYSIZEOF (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / YYSIZEOF (*yyptr);                        \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, YY_CAST (YYSIZE_T, (Count)) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYPTRDIFF_T yyi;                      \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  11
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   224

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  42
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  21
/* YYNRULES -- Number of rules.  */
#define YYNRULES  66
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  143

/* YYMAXUTOK -- Last valid token kind.  */
#define YYMAXUTOK   296


/* YYTRANSLATE(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, with out-of-bounds checking.  */
#define YYTRANSLATE(YYX)                                \
  (0 <= (YYX) && (YYX) <= YYMAXUTOK                     \
   ? YY_CAST (yysymbol_kind_t, yytranslate[YYX])        \
   : YYSYMBOL_YYUNDEF)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex.  */
static const yytype_int8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41
};

#if YYDEBUG
/* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint8 yyrline[] =
{
       0,    51,    51,    52,    56,    57,    61,    67,    76,    82,
      91,    92,    96,    97,   101,   102,   103,   104,   105,   106,
     107,   111,   118,   125,   134,   135,   136,   137,   138,   142,
     151,   155,   156,   157,   161,   162,   163,   167,   176,   179,
     182,   185,   188,   192,   193,   197,   198,   199,   203,   204,
     205,   206,   207,   211,   211,   211,   211,   211,   211,   215,
     216,   217,   220,   222,   223,   227,   228
};
#endif

/** Accessing symbol of state STATE.  */
#define YY_ACCESSING_SYMBOL(State) YY_CAST (yysymbol_kind_t, yystos[State])

#if YYDEBUG || 0
/* The user-facing name of the symbol whose (internal) number is
   YYSYMBOL.  No bounds checking.  */
static const char *yysymbol_name (yysymbol_kind_t yysymbol) YY_ATTRIBUTE_UNUSED;

/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "\"end of file\"", "error", "\"invalid token\"", "IDENTIFIER",
  "INT_CONST", "FLOAT_CONST", "STRING_CONST", "CHAR_CONST", "INT",
  "FLOAT_TYPE", "CHAR_TYPE", "DOUBLE", "VOID", "IF", "ELSE", "WHILE",
  "FOR", "RETURN", "PRINTF", "SCANF", "PLUS", "MINUS", "MULT", "DIV",
  "ASSIGN", "EQ", "NE", "LT", "GT", "LE", "GE", "AND", "OR", "NOT",
  "LPAREN", "RPAREN", "LBRACE", "RBRACE", "LBRACKET", "RBRACKET",
  "SEMICOLON", "COMMA", "$accept", "program", "external_declaration",
  "function_definition", "parameter_list", "compound_statement",
  "statement_list", "statement", "declaration", "type", "assignment",
  "expression", "term", "factor", "if_statement", "loop_statement",
  "condition", "relational_op", "function_call", "argument_list",
  "return_statement", YY_NULLPTR
};

static const char *
yysymbol_name (yysymbol_kind_t yysymbol)
{
  return yytname[yysymbol];
}
#endif

#define YYPACT_NINF (-71)

#define yypact_value_is_default(Yyn) \
  ((Yyn) == YYPACT_NINF)

#define YYTABLE_NINF (-1)

#define yytable_value_is_error(Yyn) \
  0

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
static const yytype_int16 yypact[] =
{
     209,   -71,   -71,   -71,   -71,   -71,   194,   -71,   -71,   -71,
       3,   -71,   -71,   121,    66,    80,    12,   -71,   -71,   -71,
     -71,   -71,   -71,    66,     0,    84,   -71,     1,   -28,    36,
      82,    -6,    66,    66,   -71,    66,    66,   101,   -71,     1,
     209,   -71,     6,   -71,    84,    84,   -71,   -71,    43,    69,
      92,   124,    28,   126,   141,   -71,   -71,   131,   -71,   -71,
      38,   -71,   -71,   -71,   -71,   -71,   -71,   153,   -71,    66,
      66,    66,    46,    46,   204,   -71,     5,    66,    66,   -71,
     -71,    58,   -71,     7,   115,    13,    -9,    46,    46,   102,
     122,   150,    -2,    46,    46,   -71,    60,    64,   -71,   160,
      66,   177,   120,   163,   164,   -71,   -71,   -71,   -71,   -71,
     -71,    66,    46,    46,   161,   161,    62,    93,   168,   169,
     -71,   115,    66,   -71,   115,   120,   120,   196,   -71,   208,
     208,   -71,   -71,    45,   161,   187,   188,   -71,   -71,   161,
     161,   -71,   -71
};

/* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE does not specify something else to do.  Zero
   means the default is an error.  */
static const yytype_int8 yydefact[] =
{
       0,    24,    25,    26,    27,    28,     0,     2,     4,     5,
       0,     1,     3,     0,     0,     0,     0,    21,    37,    38,
      39,    40,    41,     0,     0,    31,    34,     0,     0,     0,
       0,     0,     0,     0,    22,     0,     0,     0,     6,     0,
       0,     8,     0,    42,    32,    33,    35,    36,     0,     0,
       0,     0,     0,     0,     0,    10,    20,     0,    12,    14,
       0,    15,    16,    17,    18,    19,     7,     0,    23,     0,
      62,     0,     0,     0,     0,    66,     0,    62,    62,    11,
      13,     0,     9,     0,    63,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,    65,     0,     0,    29,     0,
       0,     0,    51,     0,     0,    53,    54,    55,    56,    57,
      58,     0,     0,     0,     0,     0,     0,     0,     0,     0,
      59,    64,     0,    52,    48,    49,    50,    43,    45,     0,
       0,    60,    61,     0,     0,     0,     0,    30,    44,     0,
       0,    47,    46
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
     -71,   -71,   218,   -71,   -71,    48,   -71,   -56,     2,     4,
     -69,   -14,   130,   151,   -71,   -71,   -70,   -71,   -71,    88,
     -71
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int8 yydefgoto[] =
{
       0,     6,     7,     8,    28,    56,    57,    58,    59,    60,
      61,    89,    25,    26,    62,    63,    90,   111,    64,    85,
      65
};

/* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule whose
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_uint8 yytable[] =
{
      24,    80,     9,    91,    10,    94,    13,    39,     9,    31,
      10,    32,    33,    40,    32,    33,    30,   102,   104,    29,
      32,    33,    69,   116,   117,    32,    33,    32,    33,    43,
     101,    18,    19,    20,    21,    22,    71,    37,    76,    41,
      34,    81,   125,   126,    67,    95,    68,    98,    99,    18,
      19,    20,    21,    22,   100,    83,    84,    86,   127,   128,
     135,   136,    23,    84,    84,    32,    33,    69,    75,    18,
      19,    20,    21,    22,   103,    38,    93,    70,   138,    87,
      88,    71,    14,   141,   142,   137,   121,    66,     1,     2,
       3,     4,     5,   112,   113,   118,    16,   124,    17,   119,
      23,   100,   129,    72,    48,   100,    35,    36,   133,     1,
       2,     3,     4,     5,    49,    27,    50,    51,    52,    53,
      54,    42,    32,    33,   112,   113,    73,   105,   106,   107,
     108,   109,   110,   130,    48,    32,    33,    37,    55,     1,
       2,     3,     4,     5,    49,    14,    50,    51,    52,    53,
      54,   112,   113,   112,   113,    15,    82,   114,    74,    16,
      77,    17,    44,    45,    48,    96,    97,    37,    79,     1,
       2,     3,     4,     5,    49,    78,    50,    51,    52,    53,
      54,   112,   113,    32,    33,   115,    46,    47,   105,   106,
     107,   108,   109,   110,    11,   112,   113,    37,    43,   123,
     120,   122,     1,     2,     3,     4,     5,    92,   131,   132,
     134,    92,     1,     2,     3,     4,     5,     1,     2,     3,
       4,     5,   139,   140,    12
};

static const yytype_uint8 yycheck[] =
{
      14,    57,     0,    73,     0,    74,     3,    35,     6,    23,
       6,    20,    21,    41,    20,    21,     4,    87,    88,    15,
      20,    21,    24,    93,    94,    20,    21,    20,    21,    35,
      39,     3,     4,     5,     6,     7,    38,    36,    52,     3,
      40,     3,   112,   113,    40,    40,    40,    40,    35,     3,
       4,     5,     6,     7,    41,    69,    70,    71,   114,   115,
     129,   130,    34,    77,    78,    20,    21,    24,    40,     3,
       4,     5,     6,     7,    88,    27,    74,    34,   134,    33,
      34,    38,    24,   139,   140,    40,   100,    39,     8,     9,
      10,    11,    12,    31,    32,    35,    38,   111,    40,    35,
      34,    41,    40,    34,     3,    41,    22,    23,   122,     8,
       9,    10,    11,    12,    13,    35,    15,    16,    17,    18,
      19,    39,    20,    21,    31,    32,    34,    25,    26,    27,
      28,    29,    30,    40,     3,    20,    21,    36,    37,     8,
       9,    10,    11,    12,    13,    24,    15,    16,    17,    18,
      19,    31,    32,    31,    32,    34,     3,    35,    34,    38,
      34,    40,    32,    33,     3,    77,    78,    36,    37,     8,
       9,    10,    11,    12,    13,    34,    15,    16,    17,    18,
      19,    31,    32,    20,    21,    35,    35,    36,    25,    26,
      27,    28,    29,    30,     0,    31,    32,    36,    35,    35,
      40,    24,     8,     9,    10,    11,    12,     3,    40,    40,
      14,     3,     8,     9,    10,    11,    12,     8,     9,    10,
      11,    12,    35,    35,     6
};

/* YYSTOS[STATE-NUM] -- The symbol kind of the accessing symbol of
   state STATE-NUM.  */
static const yytype_int8 yystos[] =
{
       0,     8,     9,    10,    11,    12,    43,    44,    45,    50,
      51,     0,    44,     3,    24,    34,    38,    40,     3,     4,
       5,     6,     7,    34,    53,    54,    55,    35,    46,    51,
       4,    53,    20,    21,    40,    22,    23,    36,    47,    35,
      41,     3,    39,    35,    54,    54,    55,    55,     3,    13,
      15,    16,    17,    18,    19,    37,    47,    48,    49,    50,
      51,    52,    56,    57,    60,    62,    47,    51,    40,    24,
      34,    38,    34,    34,    34,    40,    53,    34,    34,    37,
      49,     3,     3,    53,    53,    61,    53,    33,    34,    53,
      58,    58,     3,    50,    52,    40,    61,    61,    40,    35,
      41,    39,    58,    53,    58,    25,    26,    27,    28,    29,
      30,    59,    31,    32,    35,    35,    58,    58,    35,    35,
      40,    53,    24,    35,    53,    58,    58,    49,    49,    40,
      40,    40,    40,    53,    14,    52,    52,    40,    49,    35,
      35,    49,    49
};

/* YYR1[RULE-NUM] -- Symbol kind of the left-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr1[] =
{
       0,    42,    43,    43,    44,    44,    45,    45,    46,    46,
      47,    47,    48,    48,    49,    49,    49,    49,    49,    49,
      49,    50,    50,    50,    51,    51,    51,    51,    51,    52,
      52,    53,    53,    53,    54,    54,    54,    55,    55,    55,
      55,    55,    55,    56,    56,    57,    57,    57,    58,    58,
      58,    58,    58,    59,    59,    59,    59,    59,    59,    60,
      60,    60,    61,    61,    61,    62,    62
};

/* YYR2[RULE-NUM] -- Number of symbols on the right-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr2[] =
{
       0,     2,     1,     2,     1,     1,     5,     6,     2,     4,
       2,     3,     1,     2,     1,     1,     1,     1,     1,     1,
       1,     3,     5,     6,     1,     1,     1,     1,     1,     4,
       7,     1,     3,     3,     1,     3,     3,     1,     1,     1,
       1,     1,     3,     5,     7,     5,     8,     8,     3,     3,
       3,     2,     3,     1,     1,     1,     1,     1,     1,     5,
       5,     5,     0,     1,     3,     3,     2
};


enum { YYENOMEM = -2 };

#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYNOMEM         goto yyexhaustedlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                    \
  do                                                              \
    if (yychar == YYEMPTY)                                        \
      {                                                           \
        yychar = (Token);                                         \
        yylval = (Value);                                         \
        YYPOPSTACK (yylen);                                       \
        yystate = *yyssp;                                         \
        goto yybackup;                                            \
      }                                                           \
    else                                                          \
      {                                                           \
        yyerror (YY_("syntax error: cannot back up")); \
        YYERROR;                                                  \
      }                                                           \
  while (0)

/* Backward compatibility with an undocumented macro.
   Use YYerror or YYUNDEF. */
#define YYERRCODE YYUNDEF


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)




# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Kind, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*-----------------------------------.
| Print this symbol's value on YYO.  |
`-----------------------------------*/

static void
yy_symbol_value_print (FILE *yyo,
                       yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep)
{
  FILE *yyoutput = yyo;
  YY_USE (yyoutput);
  if (!yyvaluep)
    return;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/*---------------------------.
| Print this symbol on YYO.  |
`---------------------------*/

static void
yy_symbol_print (FILE *yyo,
                 yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyo, "%s %s (",
             yykind < YYNTOKENS ? "token" : "nterm", yysymbol_name (yykind));

  yy_symbol_value_print (yyo, yykind, yyvaluep);
  YYFPRINTF (yyo, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yy_state_t *yybottom, yy_state_t *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yy_state_t *yyssp, YYSTYPE *yyvsp,
                 int yyrule)
{
  int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %d):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       YY_ACCESSING_SYMBOL (+yyssp[yyi + 1 - yynrhs]),
                       &yyvsp[(yyi + 1) - (yynrhs)]);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args) ((void) 0)
# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif






/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg,
            yysymbol_kind_t yykind, YYSTYPE *yyvaluep)
{
  YY_USE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yykind, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/* Lookahead token kind.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;




/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    yy_state_fast_t yystate = 0;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus = 0;

    /* Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* Their size.  */
    YYPTRDIFF_T yystacksize = YYINITDEPTH;

    /* The state stack: array, bottom, top.  */
    yy_state_t yyssa[YYINITDEPTH];
    yy_state_t *yyss = yyssa;
    yy_state_t *yyssp = yyss;

    /* The semantic value stack: array, bottom, top.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs = yyvsa;
    YYSTYPE *yyvsp = yyvs;

  int yyn;
  /* The return value of yyparse.  */
  int yyresult;
  /* Lookahead symbol kind.  */
  yysymbol_kind_t yytoken = YYSYMBOL_YYEMPTY;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yychar = YYEMPTY; /* Cause a token to be read.  */

  goto yysetstate;


/*------------------------------------------------------------.
| yynewstate -- push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;


/*--------------------------------------------------------------------.
| yysetstate -- set current state (the top of the stack) to yystate.  |
`--------------------------------------------------------------------*/
yysetstate:
  YYDPRINTF ((stderr, "Entering state %d\n", yystate));
  YY_ASSERT (0 <= yystate && yystate < YYNSTATES);
  YY_IGNORE_USELESS_CAST_BEGIN
  *yyssp = YY_CAST (yy_state_t, yystate);
  YY_IGNORE_USELESS_CAST_END
  YY_STACK_PRINT (yyss, yyssp);

  if (yyss + yystacksize - 1 <= yyssp)
#if !defined yyoverflow && !defined YYSTACK_RELOCATE
    YYNOMEM;
#else
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYPTRDIFF_T yysize = yyssp - yyss + 1;

# if defined yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        yy_state_t *yyss1 = yyss;
        YYSTYPE *yyvs1 = yyvs;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * YYSIZEOF (*yyssp),
                    &yyvs1, yysize * YYSIZEOF (*yyvsp),
                    &yystacksize);
        yyss = yyss1;
        yyvs = yyvs1;
      }
# else /* defined YYSTACK_RELOCATE */
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        YYNOMEM;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yy_state_t *yyss1 = yyss;
        union yyalloc *yyptr =
          YY_CAST (union yyalloc *,
                   YYSTACK_ALLOC (YY_CAST (YYSIZE_T, YYSTACK_BYTES (yystacksize))));
        if (! yyptr)
          YYNOMEM;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YY_IGNORE_USELESS_CAST_BEGIN
      YYDPRINTF ((stderr, "Stack size increased to %ld\n",
                  YY_CAST (long, yystacksize)));
      YY_IGNORE_USELESS_CAST_END

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }
#endif /* !defined yyoverflow && !defined YYSTACK_RELOCATE */


  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;


/*-----------.
| yybackup.  |
`-----------*/
yybackup:
  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either empty, or end-of-input, or a valid lookahead.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token\n"));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = YYEOF;
      yytoken = YYSYMBOL_YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else if (yychar == YYerror)
    {
      /* The scanner already issued an error message, process directly
         to error recovery.  But do not keep the error token as
         lookahead, it is too special and may lead us to an endless
         loop in error recovery. */
      yychar = YYUNDEF;
      yytoken = YYSYMBOL_YYerror;
      goto yyerrlab1;
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);
  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  /* Discard the shifted token.  */
  yychar = YYEMPTY;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
  case 6: /* function_definition: type IDENTIFIER LPAREN RPAREN compound_statement  */
#line 61 "parser.y"
                                                     {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol((yyvsp[-3].str), (yyvsp[-4].str), "FUNCTION", "-", line_no, "0", addr);
    }
#line 1264 "parser.tab.c"
    break;

  case 7: /* function_definition: type IDENTIFIER LPAREN parameter_list RPAREN compound_statement  */
#line 67 "parser.y"
                                                                      {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol((yyvsp[-4].str), (yyvsp[-5].str), "FUNCTION", "-", line_no, "0", addr);
    }
#line 1275 "parser.tab.c"
    break;

  case 8: /* parameter_list: type IDENTIFIER  */
#line 76 "parser.y"
                    {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol((yyvsp[0].str), (yyvsp[-1].str), "PARAMETER", "-", line_no, "0", addr);
    }
#line 1286 "parser.tab.c"
    break;

  case 9: /* parameter_list: parameter_list COMMA type IDENTIFIER  */
#line 82 "parser.y"
                                           {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol((yyvsp[0].str), (yyvsp[-1].str), "PARAMETER", "-", line_no, "0", addr);
    }
#line 1297 "parser.tab.c"
    break;

  case 21: /* declaration: type IDENTIFIER SEMICOLON  */
#line 111 "parser.y"
                              {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol((yyvsp[-1].str), (yyvsp[-2].str), "IDENTIFIER", "-", line_no, "0", addr);
        strcpy(current_type, (yyvsp[-2].str));
    }
#line 1309 "parser.tab.c"
    break;

  case 22: /* declaration: type IDENTIFIER ASSIGN expression SEMICOLON  */
#line 118 "parser.y"
                                                  {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += 4;
        insert_symbol((yyvsp[-3].str), (yyvsp[-4].str), "IDENTIFIER", "-", line_no, "0", addr);
        strcpy(current_type, (yyvsp[-4].str));
    }
#line 1321 "parser.tab.c"
    break;

  case 23: /* declaration: type IDENTIFIER LBRACKET INT_CONST RBRACKET SEMICOLON  */
#line 125 "parser.y"
                                                            {
        char addr[20];
        sprintf(addr, "%d", mem_address);
        mem_address += (atoi((yyvsp[-2].str)) * 4);
        insert_symbol((yyvsp[-4].str), (yyvsp[-5].str), "ARRAY", "-", line_no, (yyvsp[-2].str), addr);
    }
#line 1332 "parser.tab.c"
    break;

  case 24: /* type: INT  */
#line 134 "parser.y"
        { (yyval.str) = strdup("int"); }
#line 1338 "parser.tab.c"
    break;

  case 25: /* type: FLOAT_TYPE  */
#line 135 "parser.y"
                 { (yyval.str) = strdup("float"); }
#line 1344 "parser.tab.c"
    break;

  case 26: /* type: CHAR_TYPE  */
#line 136 "parser.y"
                { (yyval.str) = strdup("char"); }
#line 1350 "parser.tab.c"
    break;

  case 27: /* type: DOUBLE  */
#line 137 "parser.y"
             { (yyval.str) = strdup("double"); }
#line 1356 "parser.tab.c"
    break;

  case 28: /* type: VOID  */
#line 138 "parser.y"
           { (yyval.str) = strdup("void"); }
#line 1362 "parser.tab.c"
    break;

  case 29: /* assignment: IDENTIFIER ASSIGN expression SEMICOLON  */
#line 142 "parser.y"
                                           {
        SymbolEntry *entry = lookup_symbol((yyvsp[-3].str));
        if (!entry) {
            char addr[20];
            sprintf(addr, "%d", mem_address);
            mem_address += 4;
            insert_symbol((yyvsp[-3].str), "unknown", "IDENTIFIER", "-", line_no, "0", addr);
        }
    }
#line 1376 "parser.tab.c"
    break;

  case 37: /* factor: IDENTIFIER  */
#line 167 "parser.y"
               {
        SymbolEntry *entry = lookup_symbol((yyvsp[0].str));
        if (!entry) {
            char addr[20];
            sprintf(addr, "%d", mem_address);
            mem_address += 4;
            insert_symbol((yyvsp[0].str), "unknown", "IDENTIFIER", "-", line_no, "0", addr);
        }
    }
#line 1390 "parser.tab.c"
    break;

  case 38: /* factor: INT_CONST  */
#line 176 "parser.y"
                {
        insert_symbol((yyvsp[0].str), "int", "CONSTANT", (yyvsp[0].str), line_no, "0", "-");
    }
#line 1398 "parser.tab.c"
    break;

  case 39: /* factor: FLOAT_CONST  */
#line 179 "parser.y"
                  {
        insert_symbol((yyvsp[0].str), "float", "CONSTANT", (yyvsp[0].str), line_no, "0", "-");
    }
#line 1406 "parser.tab.c"
    break;

  case 40: /* factor: STRING_CONST  */
#line 182 "parser.y"
                   {
        insert_symbol((yyvsp[0].str), "string", "CONSTANT", (yyvsp[0].str), line_no, "0", "-");
    }
#line 1414 "parser.tab.c"
    break;

  case 41: /* factor: CHAR_CONST  */
#line 185 "parser.y"
                 {
        insert_symbol((yyvsp[0].str), "char", "CONSTANT", (yyvsp[0].str), line_no, "0", "-");
    }
#line 1422 "parser.tab.c"
    break;


#line 1426 "parser.tab.c"

      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", YY_CAST (yysymbol_kind_t, yyr1[yyn]), &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */
  {
    const int yylhs = yyr1[yyn] - YYNTOKENS;
    const int yyi = yypgoto[yylhs] + *yyssp;
    yystate = (0 <= yyi && yyi <= YYLAST && yycheck[yyi] == *yyssp
               ? yytable[yyi]
               : yydefgoto[yylhs]);
  }

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYSYMBOL_YYEMPTY : YYTRANSLATE (yychar);
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
      yyerror (YY_("syntax error"));
    }

  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:
  /* Pacify compilers when the user code never invokes YYERROR and the
     label yyerrorlab therefore never appears in user code.  */
  if (0)
    YYERROR;
  ++yynerrs;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  /* Pop stack until we find a state that shifts the error token.  */
  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYSYMBOL_YYerror;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYSYMBOL_YYerror)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  YY_ACCESSING_SYMBOL (yystate), yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", YY_ACCESSING_SYMBOL (yyn), yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturnlab;


/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturnlab;


/*-----------------------------------------------------------.
| yyexhaustedlab -- YYNOMEM (memory exhaustion) comes here.  |
`-----------------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  goto yyreturnlab;


/*----------------------------------------------------------.
| yyreturnlab -- parsing is finished, clean up and return.  |
`----------------------------------------------------------*/
yyreturnlab:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  YY_ACCESSING_SYMBOL (+*yyssp), yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif

  return yyresult;
}

#line 231 "parser.y"


void insert_symbol(char *token, char *data_type, char *token_type, char *token_value, int line, char *dimension, char *address) {
    if (strcmp(token_type, "IDENTIFIER") == 0 || strcmp(token_type, "ARRAY") == 0 || strcmp(token_type, "FUNCTION") == 0) {
        SymbolEntry *curr = symbol_table;
        while (curr != NULL) {
            if (strcmp(curr->token, token) == 0 && 
                (strcmp(curr->token_type, "IDENTIFIER") == 0 || 
                 strcmp(curr->token_type, "ARRAY") == 0 || 
                 strcmp(curr->token_type, "FUNCTION") == 0)) {
                return;
            }
            curr = curr->next;
        }
    }
    
    SymbolEntry *new_entry = (SymbolEntry *)malloc(sizeof(SymbolEntry));
    strcpy(new_entry->token, token);
    strcpy(new_entry->data_type, data_type);
    strcpy(new_entry->token_type, token_type);
    strcpy(new_entry->token_value, token_value);
    new_entry->line = line;
    strcpy(new_entry->dimension, dimension);
    strcpy(new_entry->address, address);
    new_entry->next = symbol_table;
    symbol_table = new_entry;
}

SymbolEntry* lookup_symbol(char *token) {
    SymbolEntry *curr = symbol_table;
    while (curr != NULL) {
        if (strcmp(curr->token, token) == 0 && 
            (strcmp(curr->token_type, "IDENTIFIER") == 0 || 
             strcmp(curr->token_type, "ARRAY") == 0 || 
             strcmp(curr->token_type, "FUNCTION") == 0)) {
            return curr;
        }
        curr = curr->next;
    }
    return NULL;
}

void print_symbol_table() {
    printf("\n\n==================== SYMBOL TABLE ====================\n");
    printf("%-15s %-12s %-15s %-15s %-8s %-12s %-10s\n", 
           "Token", "Data Type", "Token Type", "Token Value", "Line", "Dimension", "Address");
    printf("======================================================\n");
    
    SymbolEntry *curr = symbol_table;
    while (curr != NULL) {
        printf("%-15s %-12s %-15s %-15s %-8d %-12s %-10s\n",
               curr->token, curr->data_type, curr->token_type, 
               curr->token_value, curr->line, curr->dimension, curr->address);
        curr = curr->next;
    }
    printf("======================================================\n\n");
}

void yyerror(const char *s) {
    fprintf(stderr, "Error at line %d: %s\n", line_no, s);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            printf("Could not open file %s\n", argv[1]);
            return 1;
        }
        yyin = file;
    }
    
    printf("Parsing...\n");
    yyparse();
    
    print_symbol_table();
    
    if (argc > 1) {
        fclose(yyin);
    }
    
    return 0;
}
