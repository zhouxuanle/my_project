import useLayoutStore from '../../stores/Layout/layoutStore';

export function useLayout() {
  const { isPanelOpen, setIsPanelOpen, togglePanel } = useLayoutStore();

  return {
    isPanelOpen,
    setIsPanelOpen,
    togglePanel,
  };
}
