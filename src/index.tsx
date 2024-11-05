import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  staticClasses,
  TextField,
  ToggleField
} from "@decky/ui";
import {
  callable,
  addEventListener,
  removeEventListener,
  toaster,
  definePlugin,
  // routerHook
} from "@decky/api"
import { useState } from "react";
import { FaCheckCircle, FaNetworkWired } from "react-icons/fa";

const start = callable<[], number>("start");
const stop = callable<[], void>("stop");
const getStatus = callable<[], number>("getStatus");

const setSettings = callable<[string, string, boolean], void>("setSettings");
const getSettings = callable<[], [string, string, boolean]>("getSettings");

function Content() {
  const [spoofDpiPid, setSpoofDpiPid] = useState<number | undefined>();
  const [spoofDpiPort, setSpoofDpiPort] = useState<string>();
  const [useDoh, setUseDoh] = useState<boolean>();
  const [spoofDpiDns, setSpoofDpiDns] = useState<string>();

  const onToggleSpoofDPI = async () => {
    console.log("Toggle SpoofDPI")

    if (spoofDpiPid) {
      await stop();
      setSpoofDpiPid(undefined);
    } else {
      const pid = await start();
      setSpoofDpiPid(pid);
      console.log("Started SpoofDPI with PID: " + pid);
    };
  };

  if (spoofDpiPid === undefined) {
    getStatus().then((pid) => {
      setSpoofDpiPid(pid);
    });
  }

  const setSpoofDpiConfig = async () => {
    await setSettings(spoofDpiDns || "8.8.8.8", spoofDpiPort || "9696", useDoh || false);
  };

  getSettings().then(([dns, port, useDoh]) => {
    setSpoofDpiDns(dns);
    setUseDoh(useDoh);
    setSpoofDpiPort(port);
  })

  return (
    <PanelSection title="SpoofDPI Control">
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={onToggleSpoofDPI}
        >
          {spoofDpiPid ? "Stop SpoofDPI" : "Start SpoofDPI"}
        </ButtonItem>
      </PanelSectionRow>
      <PanelSectionRow>
        {/* display running status */}

        {spoofDpiPid && (
          <div style={{ display: "flex", alignItems: "center" }}>
            <FaCheckCircle style={{ color: "green", marginRight: "8px" }} />
            <p style={{ color: "green" }}>{"SpoofDPI is running with PID: " + spoofDpiPid}</p>
          </div>
        )}
      </PanelSectionRow>

      {/* Settings */}
      <div className={staticClasses.PanelSectionTitle}>Settings</div>

      <PanelSectionRow>
        <ToggleField
          label="Use DoH"
          checked={useDoh || false}
        />
        <TextField
          label="DNS Server"
          value={spoofDpiDns}
        />
        <TextField
          label="Port"
          value={spoofDpiPort || "9696"}
        />
        <ButtonItem
          layout="below"
          onClick={setSpoofDpiConfig}
        >
          Apply Settings
        </ButtonItem>
      </PanelSectionRow>
    </PanelSection>
  );
};

export default definePlugin(() => {
  console.log("Template plugin initializing, this is called once on frontend startup")

  const restartListener = addEventListener<[]>("decky_spoof_dpi_needs_restart", () => {
    console.log("Backend has requested a restart");

    toaster.toast({
      title: "SpoofDPI Configuration Updated",
      body: "Your device will automatically restart shortly...",
    })

    setTimeout(() => {
      SteamClient.User.StartRestart(false);
    }, 5000)
  })

  return {
    name: "Decky SpoofDPI",
    titleView: <div className={staticClasses.Title}>Decky SpoofDPI</div>,
    content: <Content />,
    icon: <FaNetworkWired />,
    onDismount() {
      console.log("Unloading")
      removeEventListener("decky_spoof_dpi_needs_restart", restartListener)
    },
  };
});
