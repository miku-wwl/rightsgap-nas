"""Read only four named public documentation pages; never an API/model call."""
import hashlib
import urllib.request
import urllib.error
from phase22_common import OUT, save, now


def main():
    pages=[('rules','https://ugreenhackathon.devpost.com/rules'),
        ('resources','https://ugreenhackathon.devpost.com/resources'),
        ('starter-kit','https://ai.ugreen.com/pages/hackathon-starter-kit'),
        ('pricing','https://api-docs.deepseek.com/quick_start/pricing/')]
    records=[]
    for name,url in pages:
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RightsGap-public-documentation-check/2.2'}),timeout=30) as response:
                body=response.read()
                records.append(dict(id=name,url=url,final_url=response.url,http_status=response.status,
                    retrieved_at=now(),body_sha256=hashlib.sha256(body).hexdigest(),bytes=len(body),
                    method='Public read-only GET; no account, cookie, credential or private source',
                    full_body_not_redistributed=True))
        except urllib.error.HTTPError as error:
            records.append(dict(id=name,url=url,http_status=error.code,retrieved_at=now(),body_sha256=None,
                status='LOCAL_FETCH_BLOCKED',fallback='Live web tool already read current page during this task; no local body hash is claimed'))
    save(OUT/'official-sources.json',dict(status='WEB_VERIFIED; LOCAL_HASH_PARTIAL' if any(p.get('status')=='LOCAL_FETCH_BLOCKED' for p in records) else 'PASS',pages=records,
        initial_optional_fetch=dict(command='python -B validation/record_phase22_sources.py',exit_code=1,error='urllib.error.HTTPError: HTTP Error 403: Forbidden',retained=True),
        human_or_owner_agreement=False,source_interpretation='Relevant current requirements read with browser/web tool before draft creation; no legal consent made on owner behalf.',
        verified_requirements=dict(round1_questions=10,total_english_word_limit=500,initial_zip_max_mb=10,
            markdown_only=True,round1_nas_required=False,final_pdf_created=False,official_zip_created=False),
        current_download='https://cdn.shopify.com/s/files/1/0630/9416/1602/files/uliya-skill-kit-0.7.3-en.zip?v=1790578898',
        current_download_sha256='cf557e5a022e4297892f39768132855154232efdedeb726b2845450ccd70e1b3'))
    print('PUBLIC_DOCUMENTATION_READS_ATTEMPTED=4; LOCAL_FETCH_BLOCKS='+str(sum(p.get('status')=='LOCAL_FETCH_BLOCKED' for p in records))+'; LIVE_WEB_VERIFICATION=COMPLETE; PAID_MODEL_REQUESTS=0; CREDENTIAL_ACCESS=NO')


if __name__=='__main__':main()
