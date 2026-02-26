import idc
import idaapi

def get_transitions(state_ea):
    transitions = {}
    func_end = idc.get_func_attr(state_ea, idc.FUNCATTR_END)
    ea = state_ea

    while ea < func_end:
        mnem = idc.print_insn_mnem(ea)
        # cmp al, imm -> input char
        if mnem == "cmp" and idc.print_operand(ea, 0) == "al":
            if idc.get_operand_type(ea, 1) == idc.o_imm:
                input_char = chr(idc.get_operand_value(ea, 1))

                # jz target -> branch target
                next_insn = idc.next_head(ea)
                if idc.print_insn_mnem(next_insn).startswith("j"):
                    target = idc.get_operand_value(next_insn, 0)

                    branch_ea = target
                    next_state = None
                    while branch_ea < func_end:
                        bmnem = idc.print_insn_mnem(branch_ea)
                        op0 = idc.print_operand(branch_ea, 0)

                        if bmnem == "mov" and op0 == "ecx":
                            next_state = idc.get_operand_value(branch_ea, 1)
                        elif bmnem == "jmp" and op0 == "set_next_state":
                            if next_state is not None:
                                transitions[input_char] = next_state
                                #print(f"[DEBUG] state_{hex(state_ea)} --'{input_char}'--> state_{hex(next_state)}")
                            break
                        branch_ea = idc.next_head(branch_ea)

        ea = idc.next_head(ea)

    return transitions

def state_name_to_ea(state_name):
    ea = idc.get_name_ea_simple(state_name)
    if ea == idc.BADADDR:
        return None
    return ea

def dfs(state, depth, current):
    if depth == 0:
        print(current)
        return True
    state_ea = state_name_to_ea(state)
    transitions = get_transitions(state_ea)
    for key, val in transitions.items():
        if dfs(f"state_{str(val)}", depth-1, current+key):
            return True
        #print(f"{key}: {val}")

def main():
    # state for n has current_input == 'n'
    dfs("state_4953", 16, "")

    # or brute force
    #for i in range(100000):
    #    dfs(f"state_{i}", 16, "")

main()
