"""
Top-level rounding functions.
"""

import decimal
import fractions
import functools
import math
import struct


#: Signatures for to-nearest rounding modes
TIES_TO_ZERO = [[1, 1], [1, 1]]
TIES_TO_AWAY = [[2, 2], [2, 2]]
TIES_TO_PLUS = [[2, 2], [1, 1]]
TIES_TO_MINUS = [[1, 1], [2, 2]]
TIES_TO_EVEN = [[1, 2], [1, 2]]
TIES_TO_ODD = [[2, 1], [2, 1]]

#: Signatures for directed rounding modes
TO_ZERO = [[0, 0], [0, 0]]
TO_AWAY = [[3, 3], [3, 3]]
TO_MINUS = [[0, 0], [3, 3]]
TO_PLUS = [[3, 3], [0, 0]]
TO_EVEN = [[0, 3], [0, 3]]
TO_ODD = [[3, 0], [3, 0]]

#: Useful fractions
_TWO = fractions.Fraction(2)
_TEN = fractions.Fraction(10)


@functools.singledispatch
def decade(x) -> int:
    """
    Determine the decade that a nonzero number is contained in.

    Given nonzero x, return the unique integer e satisfying
    10**e <= abs(x) < 10**(e + 1).
    """
    # General algorithm assumes the existence of an exact conversion to Fraction.
    fx = fractions.Fraction(abs(x))
    if not fx:
        raise ValueError("decade input must be nonzero")

    n, d = fx.numerator, fx.denominator

    e = len(str(n))  # 10**(e-1) <= n < 10**e
    f = len(str(d))  # 10**(f-1) <= d < 10**f
    # Now 10**(e-f-1) < n/d < 10**(e-f+1), so the decade is either
    # e-f or e-f-1, depending on whether fx >= 10**(e-f) or not.
    return e - f if fx >= _TEN ** (e - f) else e - f - 1


@decade.register(decimal.Decimal)
def _(x) -> int:
    if not x:
        raise ValueError("decade input must be nonzero")
    if not x.is_finite():
        raise ValueError("decade input must be finite")

    return int(x.logb())


# Table mapping each integer i to the bit pattern of the smallest IEEE 754
# binary64 floating-point number whose value is at least 10**(i - 323),
# for 0 <= i < 632.

_FTEN_INTS = [
    0x0000000000000003,
    0x0000000000000015,
    0x00000000000000CB,
    0x00000000000007E9,
    0x0000000000004F11,
    0x00000000000316A3,
    0x00000000001EE257,
    0x000000000134D762,
    0x000000000C1069CE,
    0x0000000078A42206,
    0x00000004B6695433,
    0x0000002F201D49FC,
    0x000001D74124E3D2,
    0x000012688B70E62C,
    0x0000B8157268FDAF,
    0x000730D67819E8D3,
    0x0031FA182C40C60E,
    0x0066789E3750F791,
    0x009C16C5C5253576,
    0x00D18E3B9B37416A,
    0x0105F1CA820511C4,
    0x013B6E3D22865635,
    0x017124E63593F5E1,
    0x01A56E1FC2F8F359,
    0x01DAC9A7B3B73030,
    0x0210BE08D0527E1E,
    0x0244ED8B04671DA5,
    0x027A28EDC580E50E,
    0x02B059949B708F29,
    0x02E46FF9C24CB2F3,
    0x03198BF832DFDFB0,
    0x034FEEF63F97D79C,
    0x0383F559E7BEE6C2,
    0x03B8F2B061AEA072,
    0x03EF2F5C7A1A488E,
    0x04237D99CC506D59,
    0x04585D003F6488AF,
    0x048E74404F3DAADB,
    0x04C308A831868AC9,
    0x04F7CAD23DE82D7B,
    0x052DBD86CD6238DA,
    0x05629674405D6388,
    0x05973C115074BC6A,
    0x05CD0B15A491EB85,
    0x060226ED86DB3333,
    0x0636B0A8E8920000,
    0x066C5CD322B68000,
    0x06A1BA03F5B21000,
    0x06D62884F31E9400,
    0x070BB2A62FE63900,
    0x07414FA7DDEFE3A0,
    0x0775A391D56BDC88,
    0x07AB0C764AC6D3AA,
    0x07E0E7C9EEBC444A,
    0x081521BC6A6B555D,
    0x084A6A2B85062AB4,
    0x0880825B3323DAB1,
    0x08B4A2F1FFECD15D,
    0x08E9CBAE7FE805B4,
    0x09201F4D0FF10390,
    0x0954272053ED4474,
    0x098930E868E89591,
    0x09BF7D228322BAF6,
    0x09F3AE3591F5B4DA,
    0x0A2899C2F6732210,
    0x0A5EC033B40FEA94,
    0x0A9338205089F29D,
    0x0AC8062864AC6F44,
    0x0AFE07B27DD78B14,
    0x0B32C4CF8EA6B6ED,
    0x0B677603725064A8,
    0x0B9D53844EE47DD2,
    0x0BD25432B14ECEA3,
    0x0C06E93F5DA2824C,
    0x0C3CA38F350B22DF,
    0x0C71E6398126F5CC,
    0x0CA65FC7E170B33E,
    0x0CDBF7B9D9CCE00E,
    0x0D117AD428200C09,
    0x0D45D98932280F0B,
    0x0D7B4FEB7EB212CE,
    0x0DB111F32F2F4BC1,
    0x0DE5566FFAFB1EB1,
    0x0E1AAC0BF9B9E65D,
    0x0E50AB877C142FFA,
    0x0E84D6695B193BF9,
    0x0EBA0C03B1DF8AF7,
    0x0EF047824F2BB6DA,
    0x0F245962E2F6A491,
    0x0F596FBB9BB44DB5,
    0x0F8FCBAA82A16122,
    0x0FC3DF4A91A4DCB5,
    0x0FF8D71D360E13E3,
    0x102F0CE4839198DB,
    0x1063680ED23AFF89,
    0x1098421286C9BF6B,
    0x10CE5297287C2F46,
    0x1102F39E794D9D8C,
    0x1137B08617A104EF,
    0x116D9CA79D89462A,
    0x11A281E8C275CBDB,
    0x11D72262F3133ED1,
    0x120CEAFBAFD80E85,
    0x124212DD4DE70914,
    0x12769794A160CB58,
    0x12AC3D79C9B8FE2E,
    0x12E1A66C1E139EDD,
    0x1316100725988694,
    0x134B9408EEFEA839,
    0x13813C85955F2924,
    0x13B58BA6FAB6F36D,
    0x13EAEE90B964B048,
    0x1420D51A73DEEE2D,
    0x14550A6110D6A9B8,
    0x148A4CF9550C5426,
    0x14C0701BD527B498,
    0x14F48C22CA71A1BE,
    0x1529AF2B7D0E0A2D,
    0x15600D7B2E28C65C,
    0x159410D9F9B2F7F3,
    0x15C91510781FB5F0,
    0x15FF5A549627A36C,
    0x16339874DDD8C624,
    0x16687E92154EF7AD,
    0x169E9E369AA2B598,
    0x16D322E220A5B17F,
    0x1707EB9AA8CF1DDF,
    0x173DE6815302E556,
    0x1772B010D3E1CF56,
    0x17A75C1508DA432B,
    0x17DD331A4B10D3F6,
    0x18123FF06EEA847A,
    0x1846CFEC8AA52598,
    0x187C83E7AD4E6EFE,
    0x18B1D270CC51055F,
    0x18E6470CFF6546B7,
    0x191BD8D03F3E9864,
    0x1951678227871F3F,
    0x1985C162B168E70F,
    0x19BB31BB5DC320D2,
    0x19F0FF151A99F483,
    0x1A253EDA614071A4,
    0x1A5A8E90F9908E0D,
    0x1A90991A9BFA58C8,
    0x1AC4BF6142F8EEFA,
    0x1AF9EF3993B72AB9,
    0x1B303583FC527AB4,
    0x1B6442E4FB671961,
    0x1B99539E3A40DFB9,
    0x1BCFA885C8D117A7,
    0x1C03C9539D82AEC8,
    0x1C38BBA884E35A7A,
    0x1C6EEA92A61C3119,
    0x1CA3529BA7D19EB0,
    0x1CD8274291C6065B,
    0x1D0E3113363787F2,
    0x1D42DEAC01E2B4F7,
    0x1D779657025B6235,
    0x1DAD7BECC2F23AC2,
    0x1DE26D73F9D764BA,
    0x1E1708D0F84D3DE8,
    0x1E4CCB0536608D62,
    0x1E81FEE341FC585D,
    0x1EB67E9C127B6E75,
    0x1EEC1E43171A4A12,
    0x1F2192E9EE706E4B,
    0x1F55F7A46A0C89DE,
    0x1F8B758D848FAC55,
    0x1FC1297872D9CBB5,
    0x1FF573D68F903EA3,
    0x202AD0CC33744E4B,
    0x2060C27FA028B0EF,
    0x2094F31F8832DD2B,
    0x20CA2FE76A3F9475,
    0x21005DF0A267BCCA,
    0x2134756CCB01ABFC,
    0x216992C7FDC216FB,
    0x219FF779FD329CB9,
    0x21D3FAAC3E3FA1F4,
    0x2208F9574DCF8A71,
    0x223F37AD21436D0D,
    0x227382CC34CA2428,
    0x22A8637F41FCAD32,
    0x22DE7C5F127BD87F,
    0x23130DBB6B8D674F,
    0x2347D12A4670C123,
    0x237DC574D80CF16C,
    0x23B29B69070816E3,
    0x23E7424348CA1C9C,
    0x241D12D41AFCA3C3,
    0x24522BC490DDE65A,
    0x2486B6B5B5155FF1,
    0x24BC6463225AB7ED,
    0x24F1BEBDF578B2F4,
    0x25262E6D72D6DFB1,
    0x255BBA08CF8C979D,
    0x2591544581B7DEC2,
    0x25C5A956E225D673,
    0x25FB13AC9AAF4C0F,
    0x2630EC4BE0AD8F8A,
    0x2665275ED8D8F36C,
    0x269A71368F0F3047,
    0x26D086C219697E2D,
    0x2704A8729FC3DDB8,
    0x2739D28F47B4D525,
    0x277023998CD10538,
    0x27A42C7FF0054685,
    0x27D9379FEC069827,
    0x280F8587E7083E30,
    0x2843B374F06526DE,
    0x2878A0522C7E7096,
    0x28AEC866B79E0CBB,
    0x28E33D4032C2C7F5,
    0x29180C903F7379F2,
    0x294E0FB44F50586F,
    0x2982C9D0B1923745,
    0x29B77C44DDF6C516,
    0x29ED5B561574765C,
    0x2A225915CD68C9FA,
    0x2A56EF5B40C2FC78,
    0x2A8CAB3210F3BB96,
    0x2AC1EAFF4A98553E,
    0x2AF665BF1D3E6A8D,
    0x2B2BFF2EE48E0530,
    0x2B617F7D4ED8C33E,
    0x2B95DF5CA28EF40E,
    0x2BCB5733CB32B111,
    0x2C0116805EFFAEAB,
    0x2C355C2076BF9A56,
    0x2C6AB328946F80EB,
    0x2CA0AFF95CC5B093,
    0x2CD4DBF7B3F71CB8,
    0x2D0A12F5A0F4E3E5,
    0x2D404BD984990E70,
    0x2D745ECFE5BF520B,
    0x2DA97683DF2F268E,
    0x2DDFD424D6FAF031,
    0x2E13E497065CD61F,
    0x2E48DDBCC7F40BA7,
    0x2E7F152BF9F10E90,
    0x2EB36D3B7C36A91A,
    0x2EE8488A5B445361,
    0x2F1E5AACF2156839,
    0x2F52F8AC174D6124,
    0x2F87B6D71D20B96D,
    0x2FBDA48CE468E7C8,
    0x2FF286D80EC190DD,
    0x3027288E1271F514,
    0x305CF2B1970E7259,
    0x309217AEFE690778,
    0x30C69D9ABE034956,
    0x30FC45016D841BAB,
    0x3131AB20E472914B,
    0x316615E91D8F359E,
    0x319B9B6364F30305,
    0x31D1411E1F17E1E3,
    0x32059165A6DDDA5C,
    0x323AF5BF109550F3,
    0x3270D9976A5D5298,
    0x32A50FFD44F4A73E,
    0x32DA53FC9631D10D,
    0x3310747DDDDF22A8,
    0x3344919D5556EB52,
    0x3379B604AAACA627,
    0x33B011C2EAABE7D8,
    0x33E41633A556E1CE,
    0x34191BC08EAC9A42,
    0x344F62B0B257C0D2,
    0x34839DAE6F76D884,
    0x34B8851A0B548EA4,
    0x34EEA6608E29B24D,
    0x352327FC58DA0F70,
    0x3557F1FB6F10934C,
    0x358DEE7A4AD4B81F,
    0x35C2B50C6EC4F314,
    0x35F7624F8A762FD9,
    0x362D3AE36D13BBCF,
    0x366244CE242C5561,
    0x3696D601AD376ABA,
    0x36CC8B8218854568,
    0x3701D7314F534B61,
    0x37364CFDA3281E39,
    0x376BE03D0BF225C7,
    0x37A16C262777579D,
    0x37D5C72FB1552D84,
    0x380B38FB9DAA78E5,
    0x3841039D428A8B8F,
    0x38754484932D2E73,
    0x38AA95A5B7F87A0F,
    0x38E09D8792FB4C4A,
    0x3914C4E977BA1F5C,
    0x3949F623D5A8A733,
    0x398039D665896880,
    0x39B4484BFEEBC2A0,
    0x39E95A5EFEA6B348,
    0x3A1FB0F6BE50601A,
    0x3A53CE9A36F23C10,
    0x3A88C240C4AECB14,
    0x3ABEF2D0F5DA7DD9,
    0x3AF357C299A88EA8,
    0x3B282DB34012B252,
    0x3B5E392010175EE6,
    0x3B92E3B40A0E9B50,
    0x3BC79CA10C924224,
    0x3BFD83C94FB6D2AD,
    0x3C32725DD1D243AC,
    0x3C670EF54646D497,
    0x3C9CD2B297D889BD,
    0x3CD203AF9EE75616,
    0x3D06849B86A12B9C,
    0x3D3C25C268497682,
    0x3D719799812DEA12,
    0x3DA5FD7FE1796496,
    0x3DDB7CDFD9D7BDBB,
    0x3E112E0BE826D695,
    0x3E45798EE2308C3A,
    0x3E7AD7F29ABCAF49,
    0x3EB0C6F7A0B5ED8E,
    0x3EE4F8B588E368F1,
    0x3F1A36E2EB1C432D,
    0x3F50624DD2F1A9FC,
    0x3F847AE147AE147B,
    0x3FB999999999999A,
    0x3FF0000000000000,
    0x4024000000000000,
    0x4059000000000000,
    0x408F400000000000,
    0x40C3880000000000,
    0x40F86A0000000000,
    0x412E848000000000,
    0x416312D000000000,
    0x4197D78400000000,
    0x41CDCD6500000000,
    0x4202A05F20000000,
    0x42374876E8000000,
    0x426D1A94A2000000,
    0x42A2309CE5400000,
    0x42D6BCC41E900000,
    0x430C6BF526340000,
    0x4341C37937E08000,
    0x4376345785D8A000,
    0x43ABC16D674EC800,
    0x43E158E460913D00,
    0x4415AF1D78B58C40,
    0x444B1AE4D6E2EF50,
    0x4480F0CF064DD592,
    0x44B52D02C7E14AF7,
    0x44EA784379D99DB5,
    0x45208B2A2C280291,
    0x4554ADF4B7320335,
    0x4589D971E4FE8402,
    0x45C027E72F1F1282,
    0x45F431E0FAE6D722,
    0x46293E5939A08CEA,
    0x465F8DEF8808B025,
    0x4693B8B5B5056E17,
    0x46C8A6E32246C99D,
    0x46FED09BEAD87C04,
    0x4733426172C74D83,
    0x476812F9CF7920E3,
    0x479E17B84357691C,
    0x47D2CED32A16A1B2,
    0x48078287F49C4A1E,
    0x483D6329F1C35CA5,
    0x48725DFA371A19E7,
    0x48A6F578C4E0A061,
    0x48DCB2D6F618C879,
    0x4911EFC659CF7D4C,
    0x49466BB7F0435C9F,
    0x497C06A5EC5433C7,
    0x49B18427B3B4A05C,
    0x49E5E531A0A1C873,
    0x4A1B5E7E08CA3A90,
    0x4A511B0EC57E649A,
    0x4A8561D276DDFDC1,
    0x4ABABA4714957D31,
    0x4AF0B46C6CDD6E3F,
    0x4B24E1878814C9CE,
    0x4B5A19E96A19FC41,
    0x4B905031E2503DA9,
    0x4BC4643E5AE44D13,
    0x4BF97D4DF19D6058,
    0x4C2FDCA16E04B86E,
    0x4C63E9E4E4C2F345,
    0x4C98E45E1DF3B016,
    0x4CCF1D75A5709C1B,
    0x4D03726987666191,
    0x4D384F03E93FF9F5,
    0x4D6E62C4E38FF873,
    0x4DA2FDBB0E39FB48,
    0x4DD7BD29D1C87A1A,
    0x4E0DAC74463A98A0,
    0x4E428BC8ABE49F64,
    0x4E772EBAD6DDC73D,
    0x4EACFA698C95390C,
    0x4EE21C81F7DD43A8,
    0x4F16A3A275D49492,
    0x4F4C4C8B1349B9B6,
    0x4F81AFD6EC0E1412,
    0x4FB61BCCA7119916,
    0x4FEBA2BFD0D5FF5C,
    0x502145B7E285BF99,
    0x50559725DB272F80,
    0x508AFCEF51F0FB5F,
    0x50C0DE1593369D1C,
    0x50F5159AF8044463,
    0x512A5B01B605557B,
    0x516078E111C3556D,
    0x5194971956342AC8,
    0x51C9BCDFABC1357A,
    0x5200160BCB58C16D,
    0x52341B8EBE2EF1C8,
    0x526922726DBAAE3A,
    0x529F6B0F092959C8,
    0x52D3A2E965B9D81D,
    0x53088BA3BF284E24,
    0x533EAE8CAEF261AD,
    0x53732D17ED577D0C,
    0x53A7F85DE8AD5C4F,
    0x53DDF67562D8B363,
    0x5412BA095DC7701E,
    0x5447688BB5394C26,
    0x547D42AEA2879F2F,
    0x54B249AD2594C37D,
    0x54E6DC186EF9F45D,
    0x551C931E8AB87174,
    0x5551DBF316B346E8,
    0x558652EFDC6018A2,
    0x55BBE7ABD3781ECB,
    0x55F170CB642B133F,
    0x5625CCFE3D35D80F,
    0x565B403DCC834E12,
    0x569108269FD210CC,
    0x56C54A3047C694FE,
    0x56FA9CBC59B83A3E,
    0x5730A1F5B8132467,
    0x5764CA732617ED80,
    0x5799FD0FEF9DE8E0,
    0x57D03E29F5C2B18C,
    0x58044DB473335DEF,
    0x583961219000356B,
    0x586FB969F40042C6,
    0x58A3D3E2388029BC,
    0x58D8C8DAC6A0342B,
    0x590EFB1178484135,
    0x59435CEAEB2D28C1,
    0x59783425A5F872F2,
    0x59AE412F0F768FAE,
    0x59E2E8BD69AA19CD,
    0x5A17A2ECC414A040,
    0x5A4D8BA7F519C850,
    0x5A827748F9301D32,
    0x5AB7151B377C247F,
    0x5AECDA62055B2D9E,
    0x5B22087D4358FC83,
    0x5B568A9C942F3BA4,
    0x5B8C2D43B93B0A8C,
    0x5BC19C4A53C4E698,
    0x5BF6035CE8B6203E,
    0x5C2B843422E3A84D,
    0x5C6132A095CE4930,
    0x5C957F48BB41DB7C,
    0x5CCADF1AEA12525B,
    0x5D00CB70D24B7379,
    0x5D34FE4D06DE5057,
    0x5D6A3DE04895E46D,
    0x5DA066AC2D5DAEC4,
    0x5DD4805738B51A75,
    0x5E09A06D06E26113,
    0x5E400444244D7CAC,
    0x5E7405552D60DBD7,
    0x5EA906AA78B912CC,
    0x5EDF485516E7577F,
    0x5F138D352E5096B0,
    0x5F48708279E4BC5B,
    0x5F7E8CA3185DEB72,
    0x5FB317E5EF3AB328,
    0x5FE7DDDF6B095FF1,
    0x601DD55745CBB7ED,
    0x6052A5568B9F52F5,
    0x60874EAC2E8727B2,
    0x60BD22573A28F19E,
    0x60F2357684599703,
    0x6126C2D4256FFCC3,
    0x615C73892ECBFBF4,
    0x6191C835BD3F7D79,
    0x61C63A432C8F5CD7,
    0x61FBC8D3F7B3340C,
    0x62315D847AD00088,
    0x6265B4E5998400AA,
    0x629B221EFFE500D4,
    0x62D0F5535FEF2085,
    0x630532A837EAE8A6,
    0x633A7F5245E5A2CF,
    0x63708F936BAF85C2,
    0x63A4B378469B6732,
    0x63D9E056584240FE,
    0x64102C35F729689F,
    0x6444374374F3C2C7,
    0x647945145230B378,
    0x64AF965966BCE056,
    0x64E3BDF7E0360C36,
    0x6518AD75D8438F44,
    0x654ED8D34E547314,
    0x6583478410F4C7ED,
    0x65B819651531F9E8,
    0x65EE1FBE5A7E7862,
    0x6622D3D6F88F0B3D,
    0x665788CCB6B2CE0D,
    0x668D6AFFE45F8190,
    0x66C262DFEEBBB0FA,
    0x66F6FB97EA6A9D38,
    0x672CBA7DE5054486,
    0x6761F48EAF234AD4,
    0x679671B25AEC1D89,
    0x67CC0E1EF1A724EB,
    0x680188D357087713,
    0x6835EB082CCA94D8,
    0x686B65CA37FD3A0E,
    0x68A11F9E62FE4449,
    0x68D56785FBBDD55B,
    0x690AC1677AAD4AB1,
    0x6940B8E0ACAC4EAF,
    0x6974E718D7D7625B,
    0x69AA20DF0DCD3AF1,
    0x69E0548B68A044D7,
    0x6A1469AE42C8560D,
    0x6A498419D37A6B90,
    0x6A7FE52048590673,
    0x6AB3EF342D37A408,
    0x6AE8EB0138858D0A,
    0x6B1F25C186A6F04D,
    0x6B537798F4285630,
    0x6B88557F31326BBC,
    0x6BBE6ADEFD7F06AB,
    0x6BF302CB5E6F642B,
    0x6C27C37E360B3D36,
    0x6C5DB45DC38E0C83,
    0x6C9290BA9A38C7D2,
    0x6CC734E940C6F9C6,
    0x6CFD022390F8B838,
    0x6D3221563A9B7323,
    0x6D66A9ABC9424FEC,
    0x6D9C5416BB92E3E7,
    0x6DD1B48E353BCE70,
    0x6E0621B1C28AC20C,
    0x6E3BAA1E332D728F,
    0x6E714A52DFFC679A,
    0x6EA59CE797FB8180,
    0x6EDB04217DFA61E0,
    0x6F10E294EEBC7D2C,
    0x6F451B3A2A6B9C77,
    0x6F7A6208B5068395,
    0x6FB07D457124123D,
    0x6FE49C96CD6D16CC,
    0x7019C3BC80C85C7F,
    0x70501A55D07D39D0,
    0x708420EB449C8843,
    0x70B9292615C3AA54,
    0x70EF736F9B3494E9,
    0x7123A825C100DD12,
    0x7158922F31411456,
    0x718EB6BAFD91596C,
    0x71C33234DE7AD7E3,
    0x71F7FEC216198DDC,
    0x722DFE729B9FF153,
    0x7262BF07A143F6D4,
    0x72976EC98994F489,
    0x72CD4A7BEBFA31AB,
    0x73024E8D737C5F0B,
    0x7336E230D05B76CE,
    0x736C9ABD04725481,
    0x73A1E0B622C774D1,
    0x73D658E3AB795205,
    0x740BEF1C9657A686,
    0x74417571DDF6C814,
    0x7475D2CE55747A19,
    0x74AB4781EAD1989F,
    0x74E10CB132C2FF64,
    0x75154FDD7F73BF3C,
    0x754AA3D4DF50AF0B,
    0x7580A6650B926D67,
    0x75B4CFFE4E7708C1,
    0x75EA03FDE214CAF1,
    0x7620427EAD4CFED7,
    0x7654531E58A03E8C,
    0x768967E5EEC84E2F,
    0x76BFC1DF6A7A61BB,
    0x76F3D92BA28C7D15,
    0x7728CF768B2F9C5A,
    0x775F03542DFB8371,
    0x779362149CBD3227,
    0x77C83A99C3EC7EB0,
    0x77FE494034E79E5C,
    0x7832EDC82110C2FA,
    0x7867A93A2954F3B8,
    0x789D9388B3AA30A6,
    0x78D27C35704A5E68,
    0x79071B42CC5CF602,
    0x793CE2137F743382,
    0x79720D4C2FA8A031,
    0x79A6909F3B92C83E,
    0x79DC34C70A777A4D,
    0x7A11A0FC668AAC70,
    0x7A46093B802D578C,
    0x7A7B8B8A6038AD6F,
    0x7AB137367C236C66,
    0x7AE585041B2C477F,
    0x7B1AE64521F7595F,
    0x7B50CFEB353A97DB,
    0x7B8503E602893DD2,
    0x7BBA44DF832B8D46,
    0x7BF06B0BB1FB384C,
    0x7C2485CE9E7A065F,
    0x7C59A742461887F7,
    0x7C9008896BCF54FA,
    0x7CC40AABC6C32A39,
    0x7CF90D56B873F4C7,
    0x7D2F50AC6690F1F9,
    0x7D63926BC01A973C,
    0x7D987706B0213D0A,
    0x7DCE94C85C298C4D,
    0x7E031CFD3999F7B0,
    0x7E37E43C8800759C,
    0x7E6DDD4BAA009303,
    0x7EA2AA4F4A405BE2,
    0x7ED754E31CD072DA,
    0x7F0D2A1BE4048F91,
    0x7F423A516E82D9BB,
    0x7F76C8E5CA239029,
    0x7FAC7B1F3CAC7434,
    0x7FE1CCF385EBC8A0,
]

_ABS_MASK = 0x7FFF_FFFF_FFFF_FFFF
_FRACTION_MASK = 0x000F_FFFF_FFFF_FFFF


@decade.register(float)
def _(x):
    # Faster decade computation for IEEE 754 binary64 floats, suitable for
    # recoding in C.  Operates directly on the bit representation, ignoring the
    # sign bit.
    n = struct.unpack("<Q", struct.pack("<d", x))[0] & _ABS_MASK

    # Compute the binade from the bit representation.
    binade = (n >> 52) - 1023
    if binade == 1024 or n == 0:
        raise ValueError(f"Input must be finite and nonzero; got {x}")
    elif binade == -1023:
        binade = (n & _FRACTION_MASK).bit_length() - 1075
    assert _TWO ** binade <= abs(x) < _TWO ** (binade + 1)

    # Compute the decade from the binade.
    #
    # p / q = 78913 / 262144 approximates log10(2) = 0.30102999566...
    # sufficiently closely that for any integer e with abs(e) < 1651,
    #
    #     e * p // q == floor(log10(2**e))
    #
    # It follows that if (e * p) % q < q - p then
    # floor(log10(2**e)) == floor(log10(2**(e+1))) and so the binade
    # [2**e, 2**(e+1)) is entirely contained in a single decade.
    #
    # The special case that (e * p) % q == q - p can only occur if
    # (e + 1) is a multiple of q. Without our bounds on e, that can
    # only occur if e == -1. In that case, too, the binade [2**-1, 2**0)
    # is entirely contained in a single decade.
    #
    # If (e * p) % q > q - p, the binade [2**e, 2**(e+1)) straddles two
    # decades, and we need to do a comparison of n with the smallest
    # representable floating-point value that lies in the larger of those two
    # decades in order to determine which decade x lies in.

    m = binade * 78913
    decade = m >> 18
    if m & 0x3FFFF > 262144 - 78913:
        decade += _FTEN_INTS[decade + 324] <= n

    assert _TEN ** decade <= abs(x) < _TEN ** (decade + 1)
    return decade


@functools.singledispatch
def to_type_of(x, sign, significand, exponent):
    """
    Convert rounding result to type matching that of x.
    """
    raise NotImplementedError("Not implemented for general objects")


@to_type_of.register(int)
def _(x, sign, significand, exponent):
    if exponent >= 0:
        significand *= 10 ** exponent
    else:
        significand, remainder = divmod(significand, 10 ** -exponent)
        if remainder:
            raise ValueError("Not representable as an integer")
    return -significand if sign else significand


@to_type_of.register(float)
def _(x, sign, significand, exponent):
    if exponent >= 0:
        abs_value = float(significand * 10 ** exponent)
    else:
        abs_value = significand / 10 ** -exponent
    return -abs_value if sign else abs_value


@to_type_of.register(fractions.Fraction)
def _(x, sign, significand, exponent):
    if exponent >= 0:
        numerator = significand * 10 ** exponent
        denominator = 1
    else:
        numerator = significand
        denominator = 10 ** -exponent
    return (
        -fractions.Fraction(numerator, denominator)
        if sign
        else fractions.Fraction(numerator, denominator)
    )


@to_type_of.register(decimal.Decimal)
def _(x, sign, significand, exponent):
    return decimal.Decimal(f"{'-' if sign else '+'}{significand}E{exponent}")


@functools.singledispatch
def is_finite(x):
    """
    Determine whether a given object is finite.
    """
    raise NotImplementedError("Not implemented for general objects")


@is_finite.register(int)
def _(x):
    return True


@is_finite.register(float)
def _(x):
    return math.isfinite(x)


@is_finite.register(fractions.Fraction)
def _(x):
    return True


@is_finite.register(decimal.Decimal)
def _(x):
    return x.is_finite()


@functools.singledispatch
def to_quarters(x, exponent=0):
    """
    Pre-rounding step for value x, rounding to integer multiple of
    10**exponent, plus two extra bits rounded to odd.

    This base implementation works for any value that can be converted
    losslessly to a fraction, and for which signs of zero and special
    values are not a consideration.

    Returns
    -------
    negative : bool
        True for values that should be treated as negative (including
        negative zero for floating-point types), False otherwise.
    inflated_significand : int
        abs(4*x) as an integer multiple of 10**exponent, rounded to an
        integer using the round-to-odd rounding mode.
    """
    negative, x = x < 0, 4 * abs(fractions.Fraction(x))
    if exponent <= 0:
        quarters, rest = divmod(10 ** -exponent * x, 1)
    else:
        quarters, rest = divmod(x, 10 ** exponent)
    return negative, int(quarters) | bool(rest)


@to_quarters.register(float)
def _(x: fractions.Fraction, exponent: int = 0):
    if not math.isfinite(x):
        raise ValueError("Input must be finite")

    negative, x = math.copysign(1.0, x) < 0.0, fractions.Fraction(abs(x))
    if exponent <= 0:
        quarters, rest = divmod(4 * 10 ** -exponent * x, 1)
    else:
        quarters, rest = divmod(4 * x, 10 ** exponent)
    return negative, int(quarters) | bool(rest)


@to_quarters.register(decimal.Decimal)
def _(x: decimal.Decimal, exponent: int = 0):
    # XXX Tests for non-finite inputs
    # XXX Tests for preservation of sign of zero.

    if not x.is_finite():
        # XXX Is this branch even exercised?
        raise ValueError("Input must be finite")

    sign, digit_tuple, x_exponent = x.as_tuple()
    significand = int("".join(map(str, digit_tuple)))

    if x_exponent >= exponent:
        quarters, rest = 4 * significand * 10 ** (x_exponent - exponent), 0
    else:
        quarters, rest = divmod(4 * significand, 10 ** (exponent - x_exponent))
    return sign == 1, int(quarters) | bool(rest)


def _reduce(sign, inflated_significand, *, rounding_mode):
    odd = inflated_significand & 4 > 0
    return (inflated_significand + rounding_mode[sign][odd]) // 4


def round_to_figures(x, figures, *, mode=TIES_TO_EVEN):
    """
    Round a value to a given number of significant figures.

    Parameters
    ----------
    x : numeric
    figures : positive integer
    mode
        Any of the twelve available rounding modes.
    """
    if figures <= 0:
        raise ValueError(f"figures must be positive; got {figures}")

    # Special handling for infinite results.
    if not is_finite(x):
        return x

    # The choice of exponent for zero is rather arbitrary. The choice
    # here ensures alignment in a table of values expressed in
    # scientific notation, assuming that 0 is represented with
    # an exponent of zero. For example, with figures=3:
    #
    #  4.56e-02
    #  1.23e+02
    #  0.00e+00

    # XXX Can we assume that we can compare x with zero directly?
    # Do we need another singledispatch function?
    if x == 0:
        exponent = 1 - figures
    else:
        exponent = decade(x) + 1 - figures

    sign, quarters = to_quarters(x, exponent)
    significand = _reduce(sign, quarters, rounding_mode=mode)

    # Adjust if the result has one more significant figure than
    # expected due to rounding up.
    if significand == 10 ** figures:
        significand //= 10
        exponent += 1
    assert significand == 0 or 10 ** (figures - 1) <= significand < 10 ** figures

    return to_type_of(x, sign, significand, exponent)


def round_to_places(x, places, *, mode=TIES_TO_EVEN):
    """
    Round a value to a given number of places after the point.

    Parameters
    ----------
    x : numeric
    places : integer
    mode
        Any of the twelve available rounding modes.
    """
    # Special handling for infinite results.
    if not is_finite(x):
        return x

    # Figure out exponent to round to.
    exponent = -places
    sign, quarters = to_quarters(x, exponent)
    significand = _reduce(sign, quarters, rounding_mode=mode)
    return to_type_of(x, sign, significand, exponent)


def round_to_int(x, *, mode=TIES_TO_EVEN):
    """
    Round a value to the nearest integer, using the given rounding mode.

    Parameters
    ----------
    mode
        Any of the twelve available rounding modes.

    Returns
    -------
    rounded : int
    """
    if not is_finite(x):
        raise ValueError("x must be finiite")

    sign, quarters = to_quarters(x, 0)
    significand = _reduce(sign, quarters, rounding_mode=mode)
    return to_type_of(0, sign, significand, 0)


# Per-rounding-mode functions, with behaviour matching that of the built-in
# round: round to some number of places, returning a value of the same type
# as the input, or round to the nearest integer, returning an int.

def round_ties_to_away(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties away from zero.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_AWAY)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_AWAY)


def round_ties_to_zero(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties towards zero.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_ZERO)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_ZERO)


def round_ties_to_even(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    even integer.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_EVEN)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_EVEN)


def round_ties_to_odd(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties to the nearest
    odd integer.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_ODD)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_ODD)


def round_ties_to_plus(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties towards positive
    infinity.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_PLUS)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_PLUS)


def round_ties_to_minus(x, ndigits=None):
    """
    Round the input x to the nearest integer, rounding ties towards negative
    infinity.
    """
    if ndigits is None:
        return round_to_int(x, mode=TIES_TO_MINUS)
    else:
        return round_to_places(x, ndigits, mode=TIES_TO_MINUS)


def round_to_away(x, ndigits=None):
    """
    Round the input x to the nearest integer away from zero.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_AWAY)
    else:
        return round_to_places(x, ndigits, mode=TO_AWAY)


def round_to_zero(x, ndigits=None):
    """
    Round the input x to the nearest integer towards zero.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_ZERO)
    else:
        return round_to_places(x, ndigits, mode=TO_ZERO)


def round_to_plus(x, ndigits=None):
    """
    Round the input x to the nearest integer towards positive infinity.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_PLUS)
    else:
        return round_to_places(x, ndigits, mode=TO_PLUS)


def round_to_minus(x, ndigits=None):
    """
    Round the input x to the nearest integer towards negative infinity.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_MINUS)
    else:
        return round_to_places(x, ndigits, mode=TO_MINUS)


def round_to_even(x, ndigits=None):
    """
    Round the input x to the nearest even integer.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_EVEN)
    else:
        return round_to_places(x, ndigits, mode=TO_EVEN)


def round_to_odd(x, ndigits=None):
    """
    Round the input x to the nearest odd integer.
    """
    if ndigits is None:
        return round_to_int(x, mode=TO_ODD)
    else:
        return round_to_places(x, ndigits, mode=TO_ODD)
