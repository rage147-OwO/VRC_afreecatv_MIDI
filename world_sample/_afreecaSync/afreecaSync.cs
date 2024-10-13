
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;
using VRC.Udon.Common.Interfaces;


public class afreecaSync : UdonSharpBehaviour
{
    public float[] activateTime = new float[10];
    public float offTime = 1f;
    bool[] isRunning = new bool[10];
    int[] waitQueue = new int[10];
    public GameObject[] BubbleEventObject = new GameObject[10];
    public int[] range = new int[10];
    bool isMIDIMaster = false;
    void Start()
    {
        for(int i = 0; i < 10; i++)
        {
            waitQueue[i] = 0;
        }
    }
    private int Mode = 0;
    public void BubbleEvent(int Value)
    {
        
        Debug.Log("BubbleEvent : " + Value);
        //여기서 Value를 10개로 나눔
        int type = 0;
        // 어떤 range에 들어가는지 확인
        for (int i = 0; i < 10; i++)
        {
            if (Value < range[i])
            {
                type = i;
                break;
            }
        }
        if(isRunning[type])
        {
            waitQueue[type]++;
        }
        else
        {
            BubbleQueueCycle(type);
            waitQueue[type]++;
            isRunning[type] = true;
        }
    }
    public void BubbleQueueCycle(int type)
    {
        waitQueue[type] -= 1;
        SendCustomNetworkEvent(NetworkEventTarget.All,"Bubble"+type);
        SendCustomEventDelayedSeconds("BubbleOff"+type,activateTime[type]);
    }
    
    
    
    
    public void Bubble(int Value)
    {
        BubbleEventObject[Value].SetActive(true);
    }
    public void Bubble0()
    {
        Bubble(0);
    }
    public void Bubble1()
    {
        Bubble(1);
    }
    public void Bubble2()
    {
        Bubble(2);
    }
    public void Bubble3()
    {
        Bubble(3);
    }
    public void Bubble4()
    {
        Bubble(4);
    }
    public void Bubble5()
    {
        Bubble(5);
    }
    public void Bubble6()
    {
        Bubble(6);
    }
    public void Bubble7()
    {
        Bubble(7);
    }
    public void Bubble8()
    {
        Bubble(8);
    }
    public void Bubble9()
    {
        Bubble(9);
    }
    
    public void BubbleOff(int Value)
    {
        //BubbleOff 타이머에서 작동호출
        //sync On --> BubbleOffDelay --> sync Off
        //로컬에서 작동
        SendCustomNetworkEvent(NetworkEventTarget.All,"BubbleOffSync"+Value);
        SendCustomEventDelayedSeconds("isRunningOff"+Value,offTime);
    }
    public void BubbleOff0()
    {
        BubbleOff(0);
    }
    public void BubbleOff1()
    {
        BubbleOff(1);
    }
    public void BubbleOff2()
    {
        BubbleOff(2);
    }
    public void BubbleOff3()
    {
        BubbleOff(3);
    }
    public void BubbleOff4()
    {
        BubbleOff(4);
    }
    public void BubbleOff5()
    {
        BubbleOff(5);
    }
    public void BubbleOff6()
    {
        BubbleOff(6);
    }
    public void BubbleOff7()
    {
        BubbleOff(7);
    }
    public void BubbleOff8()
    {
        BubbleOff(8);
    }
    public void BubbleOff9()
    {
        BubbleOff(9);
    }
    public void BubbleOffSync(int Value)
    {
        BubbleEventObject[Value].SetActive(false);
    }
    public void BubbleOffSync0()
    {
        BubbleOffSync(0);
    }
    public void BubbleOffSync1()
    {
        BubbleOffSync(1);
    }
    public void BubbleOffSync2()
    {
        BubbleOffSync(2);
    }
    public void BubbleOffSync3()
    {
        BubbleOffSync(3);
    }
    public void BubbleOffSync4()
    {
        BubbleOffSync(4);
    }
    public void BubbleOffSync5()
    {
        BubbleOffSync(5);
    }
    public void BubbleOffSync6()
    {
        BubbleOffSync(6);
    }
    public void BubbleOffSync7()
    {
        BubbleOffSync(7);
    }
    public void BubbleOffSync8()
    {
        BubbleOffSync(8);
    }
    public void BubbleOffSync9()
    {
        BubbleOffSync(9);
    }
    public void isRunningOff(int Value)
    {
        if(waitQueue[Value] == 0)
        {
            isRunning[Value] = false;
            return;
        }
        else
        {
            BubbleQueueCycle(Value);
        }
    }
    public void isRunningOff0()
    {
        isRunningOff(0);
    }
    public void isRunningOff1()
    {
        isRunningOff(1);
    }
    public void isRunningOff2()
    {
        isRunningOff(2);
    }
    public void isRunningOff3()
    {
        isRunningOff(3);
    }
    public void isRunningOff4()
    {
        isRunningOff(4);
    }
    public void isRunningOff5()
    {
        isRunningOff(5);
    }
    public void isRunningOff6()
    {
        isRunningOff(6);
    }
    public void isRunningOff7()
    {
        isRunningOff(7);
    }
    public void isRunningOff8()
    {
        isRunningOff(8);
    }
    public void isRunningOff9()
    {
        isRunningOff(9);
    }
    
    
    
    
    
    
    

    public override void MidiNoteOn(int channel, int number, int velocity)
    {
        isMIDIMaster = true;
        if(MIDIIF(3, 1, 1, channel, number, velocity))
        {
            Mode=1;
            return;
        }
        if(MIDIIF(3, 1, 2, channel, number, velocity))
        {
            Mode=0;
            return;
        }
        if(Mode == 1)
        {
            BubbleEvent(MIDItoUshort(channel, number, velocity));
        }
    }
    
    static ushort MIDItoUshort(int channel, int number, int velocity)
    {
        return (ushort)((channel << 14) | (number << 7) | velocity);
    }
    bool MIDIIF(int targetChannel, int targetNumber, int targetVelocity,int channel,int number, int velocity)
    {
        if(channel == targetChannel && number == targetNumber && velocity == targetVelocity)
        {
            return true;
        }
        return false;
    }
}
