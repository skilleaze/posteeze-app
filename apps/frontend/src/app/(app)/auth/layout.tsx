import { getT } from '@gitroom/react/translation/get.translation.service.backend';

export const dynamic = 'force-dynamic';
import { ReactNode } from 'react';
import loadDynamic from 'next/dynamic';
import { AttributionComponent } from '@gitroom/frontend/components/auth/attribution.component';
import { LogoTextComponent } from '@gitroom/frontend/components/ui/logo-text.component';
import { MantineWrapper } from '@gitroom/react/helpers/mantine.wrapper';
import { Toaster } from '@gitroom/react/toaster/toaster';
const ReturnUrlComponent = loadDynamic(() => import('./return.url.component'));
export default async function AuthLayout({
  children,
}: {
  children: ReactNode;
}) {
  const t = await getT();

  return (
    <MantineWrapper>
      <Toaster />
      <div className="bg-[#121417] flex flex-1 p-[12px] gap-[12px] min-h-screen w-screen text-white">
        {/*<style>{`html, body {overflow-x: hidden;}`}</style>*/}
        <ReturnUrlComponent />
        <AttributionComponent />
        <div className="flex flex-col py-[40px] px-[20px] flex-1 lg:w-[600px] lg:flex-none rounded-[12px] text-white p-[12px] bg-[#1A1919]">
          <div className="w-full max-w-[440px] mx-auto justify-center gap-[20px] h-full flex flex-col text-white">
            <LogoTextComponent />
            <div className="flex">{children}</div>
            <a href="https://github.com/skilleaze/posteeze-app" target="_blank" rel="noreferrer" className="text-[12px] text-[#8A8F98] hover:text-white mt-auto">Source code</a>
          </div>
        </div>
        <div className="flex-1 hidden lg:flex flex-col items-center justify-center rounded-[12px] bg-[#1A1D21] px-[48px]">
          <div className="max-w-[520px] flex flex-col gap-[20px]">
            <div className="text-[44px] leading-[1.1] font-[800]">
              Your socials, on <span className="text-[#C6F432]">autopilot</span>.
            </div>
            <div className="text-[18px] text-[#B8BCC4] leading-[1.5]">
              Plan, write and schedule posts for every channel from one calendar. Posteeze publishes them on time.
            </div>
          </div>
        </div>
      </div>
    </MantineWrapper>
  );
}
