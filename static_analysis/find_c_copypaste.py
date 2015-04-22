#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# counts copypaste in c-like code by parsing it blockwise
#
# Usage: find_c_copypaste [path] [> _copypaste.txt]

import os, sys

MIN_COPY_LEN = 100

keywords = [word for word in """_Char16_t _Char32_t align_union alignof
   asm auto bool break case catch char class const
   const_cast constexpr continue decltype default delete do double
   dynamic_cast else enum explicit export extern
   false final float for friend goto if import inline int long
   mutable namespace new nullptr operator override private protected
   public register reinterpret_cast return short signed
   sizeof static static_cast struct switch template this
   throw true try typedef typeid typename union unsigned
   using virtual void volatile wchar_t while static_assert
   int8_t uint8_t int16_t uint16_t int32_t uint32_t int64_t uint64_t
   int_least8_t uint_least8_t int_least16_t uint_least16_t
   int_least32_t uint_least32_t int_least64_t uint_least64_t
   int_fast8_t uint_fast8_t int_fast16_t uint_fast16_t
   int_fast32_t uint_fast32_t int_fast64_t uint_fast64_t
   intptr_t uintptr_t intmax_t uintmax_t
   wint_t wchar_t wctrans_t wctype_t size_t time_t
   and and_eq bitand bitor compl not not_eq or or_eq xor xor_eq
   __gnu_cxx accumulate add_const add_cv add_lvalue_reference add_pointer add_reference add_rvalue_reference add_volatile adjacent_difference adjacent_find aligned_storage Alignment alignment_of all_of allocate_shared allocator allocator_base allocator_chunklist allocator_fixed_size allocator_newdel allocator_suballoc allocator_unbounded allocator_variable_size any_of array assign at atomic_bool atomic_char atomic_char16_t atomic_char32_t atomic_compare_exchange_strong
   atomic_compare_exchange_strong_explicit atomic_compare_exchange_weak atomic_compare_exchange_weak_explicit atomic_exchange atomic_exchange_explicit atomic_fetch_add atomic_fetch_and atomic_fetch_or atomic_fetch_sub atomic_fetch_xor atomic_int atomic_int_fast16_t atomic_int_fast32_t atomic_int_fast64_t atomic_int_fast8_t atomic_int_least16_t atomic_int_least32_t atomic_int_least64_t atomic_int_least8_t atomic_intmax_t atomic_intptr_t atomic_is_lock_free atomic_llong
   atomic_load atomic_load_explicit atomic_long atomic_ptrdiff_t atomic_schar atomic_short atomic_size_t atomic_ssize_t atomic_store atomic_store_explicit atomic_uchar atomic_uint atomic_uint_fast16_t atomic_uint_fast32_t atomic_uint_fast64_t atomic_uint_fast8_t atomic_uint_least16_t atomic_uint_least32_t atomic_uint_least64_t atomic_uint_least8_t atomic_uintmax_t atomic_uintptr_t atomic_ullong atomic_ulong atomic_ushort atomic_wchar_t auto_ptr back back_insert_iterator
   back_item bad_alloc bad_function_call bad_weak_ptr basic_filebuf basic_fstream basic_ifstream basic_ofstream basic_regex basic_streambuf basic_string begin bernoulli_distribution bidirectional_iterator_tag binary_function binary_negate binary_search bind bind1st bind2nd binder1st binder2nd binomial_distribution bit_and bit_or bit_xor bitset boost cache_chunklist cache_freelist cache_suballoc cauchy_distribution cbegin cend cerr char_traits checked_array_iterator
   checked_uninitialized_copy checked_uninitialized_fill_n chi_squared_distribution cin clear codecvt codecvt_base codecvt_byname codecvt_mode codecvt_utf16 codecvt_utf8 codecvt_utf8_utf16 collate collate_byname common_type compare_exchange_strong compare_exchange_weak complex condition_variable conditional const_iterator const_mem_fun_ref_t const_mem_fun_t const_mem_fun1_ref_t const_mem_fun1_t const_pointer_cast const_reference const_reverse_iterator copy copy_backward
   copy_if copy_n count count_if cout crbegin cref crend ctype ctype_base ctype_byname decay declare_no_pointers declare_reachable declval default_delete default_random_engine deque difference_type discard_block discard_block_engine discrete_distribution divides domain_error dynamic_pointer_cast empty enable_if enable_shared_from_this end equal equal_range equal_to EqualityComparable erase error_category error_code error_condition exception exponential_distribution extent
   extreme_value_distribution fetch_add fetch_and fetch_or fetch_sub fetch_xor filebuf fill fill_n find find_end find_first_of find_if find_if_not fisher_f_distribution float_denorm_style float_round_style for_each forward forward_iterator_tag forward_list freelist front front_insert_iterator front_item fstream function gamma_distribution generate generate_n generic_container generic_iterator generic_reverse_iterator generic_value geometric_distribution get_deleter
   get_pointer_safety get_temporary_buffer greater greater_equal has_nothrow_assign has_nothrow_constructor has_nothrow_copy has_nothrow_copy_assign has_nothrow_copy_constructor has_nothrow_default_constructor has_trivial_assign has_trivial_constructor has_trivial_copy has_trivial_copy_assign has_trivial_copy_constructor has_trivial_default_constructor has_trivial_destructor has_virtual_destructor hash hash_map hash_set ifstream includes independent_bits_engine
   initializer_list inner_product inplace_merge input_iterator_tag insert insert_iterator integral_constant invalid_argument iostream is_abstract is_arithmetic is_array is_base_of is_bind_expression is_class is_compound is_const is_constructible is_convertible is_empty is_enum is_error_code_enum is_error_condition_enum is_explicitly_convertible is_floating_point is_function is_fundamental is_heap is_heap_until is_integral is_literal_type is_lock_free is_lvalue_reference
   is_member_function_pointer is_member_object_pointer is_member_pointer is_nothrow_constructible is_object is_partitioned is_placeholder is_pod is_pointer is_polymorphic is_reference is_rvalue_reference is_same is_scalar is_signed is_sorted is_sorted_until is_standard_layout is_trivial is_union is_unsigned is_void is_volatile istream istream_iterator istreambuf_iterator iter_swap iterator iterator_traits knuth_b length_error less less_equal LessThanComparable
   lexicographical_compare linear_congruential linear_congruential_engine list locale logic_error logical_and logical_not logical_or lognormal_distribution lower_bound make_checked_array_iterator make_heap make_shared make_signed make_unsigned map match_results max max_element max_fixed_size max_none max_unbounded max_variable_size mem_fn mem_fun mem_fun_ref mem_fun_ref_t mem_fun_t mem_fun1_ref_t mem_fun1_t merge mersenne_twister mersenne_twister_engine messages
   messages_base messages_byname min min_element minmax minmax_element minstd_rand minstd_rand0 minus mismatch modulus money_base money_get money_put moneypunct moneypunct_byname move move_backward move_iterator mt19937 mt19937_64 multimap multiplies multiset negate negative_binomial_distribution new_handler next_permutation none_of normal_distribution not_equal_to not1 not2 nothrow nothrow_t nth_element num_get num_put numeric_limits numpunct numpunct_byname ofstream
   ostream_iterator ostreambuf_iterator out_of_range output_iterator_tag overflow_error owner_less pair partial_sort partial_sort_copy partial_sum partition partition_copy partition_point piecewise_constant_distribution piecewise_linear_distribution plus pointer_safety pointer_to_binary_function pointer_to_unary_function poisson_distribution pop_back pop_front pop_heap prev_permutation priority_queue ptr_fun push_back push_front push_heap queue random_access_iterator_tag
   random_device random_shuffle range_error rank ranlux_base_01 ranlux24 ranlux24_base ranlux3 ranlux3_01 ranlux4 ranlux4_01 ranlux48 ranlux48_base ranlux64_base_01 ratio ratio_add ratio_divide ratio_multiply ratio_subtract raw_storage_iterator rbegin ref reference reference_wrapper regex regex_constants regex_error regex_iterator regex_token_iterator regex_traits remove remove_all_extents remove_const remove_copy remove_copy_if remove_cv remove_extent remove_if
   remove_pointer remove_reference remove_volatile rend replace replace_copy replace_copy_if replace_if requires resize result_of return_temporary_buffer reverse reverse_copy reverse_iterator rotate rotate_copy rts_alloc runtime_error search search_n seed_seq set set_difference set_intersection set_new_handler set_symmetric_difference set_union shared_ptr shuffle_order_engine size size_type sort sort_heap stable_partition stable_sort stack static_pointer_cast std string
   student_t_distribution sub_match subtract_with_carry subtract_with_carry_01 subtract_with_carry_engine swap swap_ranges sync_none sync_per_container sync_per_thread sync_shared system_error time_base time_get time_get_byname time_put time_put_byname to_array tr1 transform tuple tuple_element tuple_size type_info unary_function unary_negate unchecked_uninitialized_copy unchecked_uninitialized_fill_n undeclare_no_pointers undeclare_reachable underflow_error uniform_int
   uniform_int_distribution uniform_real uniform_real_distribution uninitialized_copy uninitialized_copy_n uninitialized_fill uninitialized_fill_n unique unique_copy unique_ptr unordered_map unordered_multimap unordered_multiset unordered_set upper_bound valarray value_type variate_generator vector wcerr wcin wcout weak_ptr weibull_distribution wfilebuf wfstream wifstream wiostream wistream wofstream wregex xor_combine
""".replace('\n', ' ').split(' ') if word != '']



def get_block_intervals_from_source( text ):
        blocks = []     # (from , to)
        block_stack = [] # from
        last_char = ''
        slashed_comment_mode = False
        bracket_comment_mode = False
        
        for i, char in enumerate(text):
        
                if last_char == '/' and char == '/':
                        slashed_comment_mode = True
                if char == '\n':
                        slashed_comment_mode = False
        
                if last_char == '/' and char == '*':
                        bracket_comment_mode = True
                if last_char == '*' and char == '/':
                        bracket_comment_mode = False
                        
                last_char = char
                
                if bracket_comment_mode or slashed_comment_mode:
                        continue

                if char == '{':
                        block_stack += [i]
                if char == '}':
                        if block_stack == []:
                                return 'Parsing error'
                        blocks += [(block_stack[-1] + 1, i)]
                        block_stack = block_stack[:-1]

        return blocks


def straighten_block( text ):
        text = text.strip()
        text = text.replace('\t', ' ')
        text = text.replace('\n', ' ')
        while text.find('  ') > -1:
                text = text.replace('  ', ' ')
        return text             


def ok_for_a_term( char ):
        return char in '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'


def ok_to_start_a_term( char ):
        return char in '_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

        
def determinize_block( text ):
        terms = {}      # term: no
        in_term = False
        term = ""
        last_char = ''
        slashed_comment_mode = False
        bracket_comment_mode = False

        for char in text:
                if last_char == '/' and char == '/':
                        slashed_comment_mode = True
                if char == '\n':
                        slashed_comment_mode = False
        
                if last_char == '/' and char == '*':
                        bracket_comment_mode = True
                if last_char == '*' and char == '/':
                        bracket_comment_mode = False
                        
                last_char = char
                
                if bracket_comment_mode or slashed_comment_mode:
                        continue

                if not in_term and ok_to_start_a_term( char ):
                        in_term = True
                if in_term and not ok_for_a_term( char ):
                        in_term = False
                        if not term in terms:
                                if not term in keywords:
                                        terms[term] = len( terms )
                        term = ''
                        
                if in_term:
                        term += char

        for term, i in terms.items():
                text = text.replace( term, '$$$' + str(i) + '$$$' )
                
        text = text.replace(' ', '')

        return text
        


copies = {} # hashable: [(file_name, a, b, text1), (file_name, c,d, text2), ...]
char_count = 0
pasted_char_count = 0
                        
def collect_all(where = "."):
        ls = os.listdir(where)
        for l in ls:    
                if l == "count_copypaste.py":
                        continue
                path = where + '/' + l
                if os.path.isfile( path ):
                        (root, ext) = os.path.splitext( path )
                        if ext.upper() == ".CPP" or ext.upper() == ".H" or ext.upper() == ".C" or \
                        ext.upper() == ".CC" or ext.upper() == ".HH" or ext.upper() == ".HPP" or \
                        ext.upper() == ".CS" or ext.upper() == ".JAVA":
                                sys.stderr.write( path + '\n')

                                global copies                           
                                global char_count
                                global pasted_char_count

                                f = open(path)
                                text = f.read()
                                f.close()
                                char_count += len( text )
        
                                blocks_or_error = get_block_intervals_from_source( text )
                                if blocks_or_error == 'Parsing error':
                                        sys.stderr.write( '!!! Error parsing ' + path + '\n')
                                        continue

                                for (a, b) in blocks_or_error:
                                        hashable = determinize_block(straighten_block( text[a:b] ))
                                        if hashable == '':
                                                continue
                                        if hashable in copies:
                                                copies[hashable] += [(path, a, b, text[a: b])]
                                                if (b-a) >= MIN_COPY_LEN:
                                                        pasted_char_count += (b-a)
                                        else:
                                                copies[hashable] = [(path, a, b, text[a: b])]
                        
                if os.path.isdir( path ):
                        collect_all( path )
                        

if len(sys.argv) > 2:
        print "Usage: find_c_copypaste [path] [> _copypaste.txt]"
        sys.exit(1)

collect_all(sys.argv[1] if len(sys.argv) > 1 else ".")


for _, list_of_pastes in sorted(copies.items(), key = lambda item: len(item[1][0][-1])):
        if len( list_of_pastes ) > 1 and len(list_of_pastes[0][-1]) > MIN_COPY_LEN:
                print '\n\n\n\n\n'
                for (file_name, a, b, text) in list_of_pastes:
                        print 'In', file_name + ':', a, '-', b, '\n', text, '\n\n'
                        
if char_count != 0:
        print "Total char count:", char_count
        print "Copy-pasted char count:", pasted_char_count
        print 'Ratio %:', (pasted_char_count * 10000 / char_count) / 100.0
else:
        print 'No source files found.'