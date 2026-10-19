import os, io, shutil
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject
from reportlab.pdfgen import canvas

SOURCE_PDF = r'C:\Users\rosha\Downloads\Society Service Connect Mini project.pdf'
OUTPUT_DIR = r'C:\Roshan\Antigravity\Mini Project\Society_Sync_Project_Reports'
DOWNLOADS_DIR = r'C:\Users\rosha\Downloads'

TEAM_FILENAME = 'Society_Sync_Project_Report_Team_Combined.pdf'

REPLACEMENTS = {
    0: [
        (b'[(SOCIETY)37( )5.0000007(S)4(ER)35(VICE )5.0000007(C)3(ONNE)4(CT)]TJ', b'[]TJ'),
        (b'[(Pri)-3.0000003(n)-3.0000003(ce )61.000005(A)4(s)-3.0000003(h)4(o)4(k)-3.0000003( Dube)6.0000007(y)]TJ', b'[]TJ'),
        (b'[(303)]TJ', b'[]TJ'),
    ],
    1: [
        (b'[<00B3>-3.0000003<00360052>5.0000007<0046004C>-3.0000003<0048>8<0057005C>4<0003>-99.00001<003600480055>8<0059>-3.0000003<004C>-3.0000003<0046>8<00480003>-91.00001<0026>-3.0000003<0052>4<0051005100480046005700B4>]TJ', b'[]TJ'),
        (b'[(P)4(r)8(i)-3.0000003(nce As)-6.0000007(h)9(o)-3.0000003(k )-31(D)-3.0000003(ubey)5.0000007( )]TJ', b'[]TJ'),
        (b'[(303)]TJ', b'[]TJ'),
    ],
    2: [
        (b'[(So)-3.0000003(c)8(i)-3.0000003(et)4(y)-3.0000003( )-202.00002(Ser)8(v)-3.0000003(i)4(ce )-203.00002(Co)5.0000007(n)4(n)-3.0000003(ec)8(t)-3.0000003( )-202.00002(\\(SSC\\) )-201(i)4(s)-3.0000003( )-202.00002(a )-202.00002(w)-3.0000003(e)8(b)4( )-202.00002(an)-4(d)-3.0000003( )-202.00002(m)9(o)-3.0000003(b)4(i)4(l)-3.0000003(e )-202.00002(p)4(l)-3.0000003(at)4(fo)-4(r)8(m )-202.00002(t)-3.0000003(h)-3.0000003(a)8(t)-3.0000003( )-202.00002(co)4(n)4(n)-3.0000003(ec)8(t)4(s)4( )]TJ', b'[]TJ'),
    ],
    3: [
        (b'[(K)-3.0000003(e)8(y)-3.0000003(w)4(o)-3.0000003(r)8(d)-3.0000003(s)4(:)-3.0000003( )-236(So)-3.0000003(c)8(i)-3.0000003(e)8(t)-3.0000003(y)-3.0000003( )-228.00002(Serv)4(i)-3.0000003(ce )-237(Co)5.0000007(n)4(n)-3.0000003(ec)8(t)-3.0000003(, )-234.00003(H)4(o)-3.0000003(u)4(s)4(i)-3.0000003(n)4(g)-3.0000003( )-236(So)-3.0000003(c)8(i)-3.0000003(e)8(t)-3.0000003(y)64(, )-234.00003(Serv)4(i)-3.0000003(ce )-237(Mar)8(k)-3.0000003(et)4(p)4(l)-3.0000003(ace,)9( )]TJ', b'[]TJ'),
    ],
    4: [
        (b'[(g)4(u)4(i)-3.0000003(d)-3.0000003(a)8(n)-3.0000003(c)8(e an)6.0000007(d)-3.0000003( )11.000001(s)-3.0000003(u)4(p)4(p)-3.0000003(o)-3.0000003(r)8(t)-3.0000003( t)7(h)-3.0000003(r)8(o)4(u)-3.0000003(g)4(h)4(o)-3.0000003(u)4(t)-3.0000003( t)7(h)4(e de)6.0000007(v)-3.0000003(el)4(o)4(p)-3.0000003(me)8(n)-3.0000003(t)-3.0000003( )11.000001(o)-3.0000003(f t)6.0000007(h)-3.0000003(e )10.000001(So)-3.0000003(c)8(i)-3.0000003(et)4(y)-3.0000003( Ser)10.000001(v)4(i)-3.0000003(ce)]TJ', b'[]TJ'),
        (b'[(C)4(o)4(n)4(n)-3.0000003(ec)8(t)-3.0000003( p)-3.0000003(ro)4(j)-3.0000003(ec)8(t)-3.0000003(.)]TJ', b'[]TJ'),
    ],
    5: [
        (b'[(I )-100(h)-3.0000003(ere)7(b)-3.0000003(y)-3.0000003( )-91.00001(d)-3.0000003(ec)8(l)-3.0000003(are )-92.00001(t)-3.0000003(h)4(at)4( )-99.00001(t)-3.0000003(h)-3.0000003(e )-91.00001(p)-3.0000003(ro)4(j)-3.0000003(ec)8(t)-3.0000003( )-99.00001(e)8(n)-3.0000003(t)4(i)-3.0000003(t)4(l)-3.0000003(e)8(d)-3.0000003( )-99.00001("So)-5.0000007(c)8(i)-3.0000003(e)8(t)-3.0000003(y)-3.0000003( )-99.00001(Se)9(rv)4(i)-3.0000003(ce )-100(C)9(o)4(n)-3.0000003(n)4(ect)-4( )-99.00001(\\(SS)9(C\\)" )-93.00001(h)-3.0000003(a)8(s)4( )]TJ', b'[]TJ'),
    ],
    7: [
        (b'[(So)-3.0000003(c)8(i)-3.0000003(et)4(y)-3.0000003( )-219.00002(S)9(erv)3.0000003(i)-3.0000003(ce)8( )-219.00002(Co)5.0000007(n)4(n)-3.0000003(ec)8(t)-3.0000003( )-219.00002(\\(SSC)9(\\) )-219.00002(i)4(s)-3.0000003( )-219.00002(a )-211(d)4(i)-3.0000003(g)4(i)4(t)-3.0000003(al)4( )-219.00002(mar)8(k)-3.0000003(e)8(t)-3.0000003(p)4(l)-3.0000003(ac)8(e )-220.00002(t)4(h)-3.0000003(a)8(t)4( )-219.00002(ag)4(g)-3.0000003(re)8(g)-3.0000003(a)8(t)-3.0000003(es)4( )-219.00002(t)4(h)-3.0000003(i)4(s)4( )]TJ', b'[]TJ'),
    ],
    31: [
        (b'[(So)-3.0000003(c)8(i)-3.0000003(et)4(y)-3.0000003( )-185(Ser)8(v)4(i)-3.0000003(ce )-186.00002(C)9(o)4(n)4(n)-3.0000003(ec)8(t)-3.0000003( )-185(p)-3.0000003(r)8(o)4(p)-3.0000003(o)4(s)-3.0000003(e)8(s)-3.0000003( )-185(a )-185(s)4(i)-3.0000003(m)9(p)-3.0000003(l)-3.0000003(e )-177.00002(b)4(u)-3.0000003(t)-3.0000003( )]TJ', b'[]TJ'),
    ]
}

def make_team_overlay(page_idx, page_width, page_height):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    
    # -------------------------------------------------------------
    # PAGE 1 (Index 0): Title & All 5 Team Members
    # -------------------------------------------------------------
    if page_idx == 0:
        # Title
        can.setFillColorRGB(1, 1, 1)
        can.rect(50, 740, 495, 35, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)
        can.setFont('Times-Bold', 23.04)
        can.drawCentredString(page_width / 2.0, 748.3, 'SOCIETY SYNC')
        
        # Whiteout student name and roll area
        can.setFillColorRGB(1, 1, 1)
        can.rect(80, 500, 435, 68, fill=1, stroke=0)
        
        # Draw all 5 members centered under "By"
        can.setFillColorRGB(0, 0, 0)
        team_members = [
            'Prince Dubey (TCS303)',
            'Sharwari Kamlesh Narvekar (TCS322)',
            'Roshan Prajapati (TCS327)',
            'Sonali Rawat (TCS330)',
            'Poorva Desai (TCS348)'
        ]
        
        start_y = 562.0
        step_y = 13.0
        can.setFont('Times-Roman', 11.5)
        for idx, m in enumerate(team_members):
            can.drawCentredString(page_width / 2.0, start_y - (idx * step_y), m)

    # -------------------------------------------------------------
    # PAGE 2 (Index 1): Certificate with All 5 Members
    # -------------------------------------------------------------
    elif page_idx == 1:
        # Whiteout certificate body
        can.setFillColorRGB(1, 1, 1)
        can.rect(70, 475, 455, 105, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)
        
        # Line 1:
        to1 = can.beginText(73.46, 568.0)
        to1.setFont('Times-Roman', 13.0)
        to1.textOut('This is to certify that the project entitled, ')
        to1.setFont('Times-Bold', 13.0)
        to1.textOut('\u201cSociety Sync\u201d')
        to1.setFont('Times-Roman', 13.0)
        to1.textOut(', is bona fide work of:')
        can.drawText(to1)
        
        # Line 2:
        to2 = can.beginText(73.46, 549.0)
        to2.setFont('Times-Bold', 13.0)
        to2.textOut('Prince Dubey ')
        to2.setFont('Times-Roman', 13.0)
        to2.textOut('(TCS303), ')
        to2.setFont('Times-Bold', 13.0)
        to2.textOut('Sharwari Kamlesh Narvekar ')
        to2.setFont('Times-Roman', 13.0)
        to2.textOut('(TCS322),')
        can.drawText(to2)
        
        # Line 3:
        to3 = can.beginText(73.46, 530.0)
        to3.setFont('Times-Bold', 13.0)
        to3.textOut('Roshan Prajapati ')
        to3.setFont('Times-Roman', 13.0)
        to3.textOut('(TCS327), ')
        to3.setFont('Times-Bold', 13.0)
        to3.textOut('Sonali Rawat ')
        to3.setFont('Times-Roman', 13.0)
        to3.textOut('(TCS330) and ')
        to3.setFont('Times-Bold', 13.0)
        to3.textOut('Poorva Desai ')
        to3.setFont('Times-Roman', 13.0)
        to3.textOut('(TCS348),')
        can.drawText(to3)
        
        # Line 4:
        can.setFont('Times-Roman', 13.0)
        can.drawString(73.46, 511.0, 'submitted in partial fulfillment of the requirements for the award of degree of')
        
        # Line 5:
        can.setFont('Times-Roman', 13.0)
        can.drawString(73.46, 492.0, 'BACHELOR OF SCIENCE in COMPUTER SCIENCE from University of Mumbai.')

    # -------------------------------------------------------------
    # PAGE 3 (Index 2): Abstract
    # -------------------------------------------------------------
    elif page_idx == 2:
        can.setFillColorRGB(1, 1, 1)
        can.rect(70, 456, 455, 18, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)
        can.setFont('Times-Roman', 14.04)
        can.drawString(72.0, 460.9, 'Society Sync (SSC) is a web and mobile platform that connects ')

    # -------------------------------------------------------------
    # PAGE 4 (Index 3): Keywords
    # -------------------------------------------------------------
    elif page_idx == 3:
        can.setFillColorRGB(1, 1, 1)
        can.rect(70, 598, 455, 18, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)
        can.setFont('Times-Roman', 14.04)
        can.drawString(72.0, 603.5, 'Keywords: Society Sync, Housing Society, Service Marketplace, ')

    # -------------------------------------------------------------
    # PAGE 5 (Index 4): Acknowledgement
    # -------------------------------------------------------------
    elif page_idx == 4:
        can.setFillColorRGB(1, 1, 1)
        can.rect(70, 666, 455, 18, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)
        can.setFont('Times-Roman', 14.04)
        can.drawString(72.0, 671.6, 'for her guidance and support throughout the development of the Society Sync')
        
        can.setFillColorRGB(1, 1, 1)
        can.rect(70, 650, 150, 18, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)
        can.drawString(72.0, 654.6, 'project.')

    # -------------------------------------------------------------
    # PAGE 6 (Index 5): Declaration
    # -------------------------------------------------------------
    elif page_idx == 5:
        can.setFillColorRGB(1, 1, 1)
        can.rect(70, 701, 455, 18, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)
        can.setFont('Times-Roman', 14.04)
        can.drawString(71.3, 705.7, 'I hereby declare that the project entitled "Society Sync (SSC)" has ')

    # -------------------------------------------------------------
    # PAGE 8 (Index 7): Introduction
    # -------------------------------------------------------------
    elif page_idx == 7:
        can.setFillColorRGB(1, 1, 1)
        can.rect(70, 513, 455, 18, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)
        can.setFont('Times-Roman', 14.04)
        can.drawString(72.0, 518.2, 'Society Sync (SSC) is a digital marketplace that aggregates this ')

    # -------------------------------------------------------------
    # PAGE 32 (Index 31): Conclusion
    # -------------------------------------------------------------
    elif page_idx == 31:
        can.setFillColorRGB(1, 1, 1)
        can.rect(70, 703, 455, 18, fill=1, stroke=0)
        can.setFillColorRGB(0, 0, 0)
        can.setFont('Times-Roman', 14.04)
        can.drawString(72.0, 707.9, 'Society Sync proposes a simple but effective idea: aggregate the ')

    can.save()
    packet.seek(0)
    return packet

def build_team_report():
    reader = PdfReader(SOURCE_PDF)
    writer = PdfWriter()
    
    total_pages = len(reader.pages)
    
    for i in range(total_pages):
        page = reader.pages[i]
        pw = float(page.mediabox.width)
        ph = float(page.mediabox.height)
        
        # 1. Clean the stream bytes directly from raw /Contents
        if i in REPLACEMENTS:
            raw = page['/Contents']
            streams = list(raw) if isinstance(raw, ArrayObject) else [raw]
            for s_obj in streams:
                actual = s_obj.get_object()
                if hasattr(actual, 'get_data'):
                    d = actual.get_data()
                    for old_pat, new_pat in REPLACEMENTS[i]:
                        d = d.replace(old_pat, new_pat)
                    actual.set_data(d)
        
        # 2. Composite visual layer with all 5 team members
        if i in [0, 1, 2, 3, 4, 5, 7, 31]:
            overlay_stream = make_team_overlay(i, pw, ph)
            overlay_pdf = PdfReader(overlay_stream)
            page.merge_page(overlay_pdf.pages[0])
            
        writer.add_page(page)
        
    out_path = os.path.join(OUTPUT_DIR, TEAM_FILENAME)
    with open(out_path, 'wb') as f:
        writer.write(f)
        
    downloads_path = os.path.join(DOWNLOADS_DIR, TEAM_FILENAME)
    shutil.copy2(out_path, downloads_path)
    
    file_size = os.path.getsize(out_path)
    print(f"Generated 6th Team Report: {TEAM_FILENAME} ({file_size} bytes, {total_pages} pages)")
    print(f"   -> Copied to: {downloads_path}")

if __name__ == '__main__':
    build_team_report()
